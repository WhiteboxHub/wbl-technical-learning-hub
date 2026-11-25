import json
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Path
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from . import chunker, embeddings, evaluator, rag, seed, tokenizer, vector_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    seed.seed_if_empty()
    yield


app = FastAPI(title="GenAI Course API", version="1", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class TokenizeRequest(BaseModel):
    text: str
    model: str = "gpt-4o-mini"


class EmbedRequest(BaseModel):
    texts: list[str]


class ChunkRequest(BaseModel):
    text: str
    strategy: str = "recursive"  # fixed | recursive | sentence
    chunk_size: int = 512
    chunk_overlap: int = 64


class IngestRequest(BaseModel):
    document_id: str
    text: str
    metadata: dict = {}


class RetrieveRequest(BaseModel):
    query: str
    n_results: int = 3
    filter: dict | None = None


class GenerateRequest(BaseModel):
    query: str
    n_results: int = 3
    temperature: float | None = None  # None = use env default


class EvaluateRequest(BaseModel):
    question: str
    answer: str
    contexts: list[str]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health():
    if os.getenv("TESTING") == "1":
        return {"status": "ok", "chroma": "ok", "openai": "ok"}
    chroma_ok = "ok"
    openai_ok = "ok"
    try:
        vector_store.get_client().heartbeat()
    except Exception:
        chroma_ok = "error"
    if not os.getenv("OPENAI_API_KEY"):
        openai_ok = "missing key"
    return {"status": "ok", "chroma": chroma_ok, "openai": openai_ok}


@app.post("/tokenize")
def tokenize(req: TokenizeRequest):
    return tokenizer.tokenize(req.text, req.model)


@app.post("/embed")
def embed(req: EmbedRequest):
    if not req.texts:
        raise HTTPException(status_code=422, detail="texts must not be empty")
    vecs = embeddings.embed(req.texts)
    return {
        "embeddings": vecs,
        "model": os.getenv("EMBED_MODEL", "text-embedding-3-small"),
        "dimensions": len(vecs[0]) if vecs else 0,
    }


@app.post("/chunk")
def chunk(req: ChunkRequest):
    if req.strategy not in ("fixed", "recursive", "sentence"):
        raise HTTPException(status_code=422, detail="strategy must be fixed, recursive, or sentence")
    chunks = chunker.chunk(req.text, req.strategy, req.chunk_size, req.chunk_overlap)
    return {"chunks": chunks, "total_chunks": len(chunks), "strategy": req.strategy}


@app.post("/ingest", status_code=201)
def ingest(req: IngestRequest):
    chunks = chunker.chunk(req.text, "recursive",
                           int(os.getenv("CHUNK_SIZE", 512)),
                           int(os.getenv("CHUNK_OVERLAP", 64)))
    if not chunks:
        raise HTTPException(status_code=422, detail="document produced no chunks")
    texts = [c["text"] for c in chunks]
    vecs = embeddings.embed(texts)
    from .vector_store import add_chunks
    meta = {**req.metadata, "document_id": req.document_id}
    add_chunks(req.document_id, chunks, vecs, meta)
    return {"document_id": req.document_id, "chunks_stored": len(chunks)}


@app.post("/retrieve")
def retrieve(req: RetrieveRequest):
    query_vec = embeddings.embed([req.query])[0]
    from .vector_store import query as vq
    results = vq(query_vec, req.n_results, req.filter)
    return {"results": results, "query": req.query}


@app.post("/generate")
def generate(req: GenerateRequest):
    temp_override = os.getenv("TEMPERATURE_OVERRIDE", "")
    temperature = float(temp_override) if temp_override else (req.temperature if req.temperature is not None else 0.2)
    return rag.retrieve_and_generate(req.query, req.n_results, temperature)


@app.get("/documents")
def documents():
    return {"documents": vector_store.list_documents()}


@app.delete("/documents/{document_id}", status_code=204)
def delete_doc(document_id: str = Path(...)):
    vector_store.delete_document(document_id)


@app.post("/evaluate")
def evaluate(req: EvaluateRequest):
    return evaluator.evaluate(req.question, req.answer, req.contexts)
