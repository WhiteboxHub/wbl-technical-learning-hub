"""ChromaDB interface — Module 3 demos."""
import os
from typing import Any
import chromadb

_client: Any = None
COLLECTION_NAME = "hr_documents"


def get_client() -> Any:
    global _client
    if _client is None:
        host = os.getenv("CHROMA_HOST", "vector-db")
        port = int(os.getenv("CHROMA_PORT", "8000"))
        _client = chromadb.HttpClient(host=host, port=port)
    return _client


def get_collection():
    return get_client().get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def add_chunks(document_id: str, chunks: list[dict],
               embeddings_list: list[list[float]], metadata: dict) -> None:
    col = get_collection()
    ids = [f"{document_id}__chunk_{i}" for i in range(len(chunks))]
    documents = [c["text"] for c in chunks]
    metadatas = [{**metadata, "chunk_index": i, "token_count": c["token_count"]}
                 for i, c in enumerate(chunks)]
    col.upsert(ids=ids, embeddings=embeddings_list,
               documents=documents, metadatas=metadatas)


def query(query_embedding: list[float], n_results: int = 3,
          filter_meta: dict | None = None) -> list[dict]:
    col = get_collection()
    kwargs = dict(query_embeddings=[query_embedding], n_results=n_results,
                  include=["documents", "metadatas", "distances"])
    if filter_meta:
        kwargs["where"] = filter_meta
    results = col.query(**kwargs)
    out = []
    for doc, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0],
    ):
        # Chroma cosine distance: similarity = 1 - distance
        score = round(1.0 - dist, 4)
        out.append({
            "text": doc,
            "score": score,
            "document_id": meta.get("document_id", "unknown"),
            "metadata": meta,
        })
    return out


def delete_document(document_id: str) -> None:
    col = get_collection()
    col.delete(where={"document_id": document_id})


def list_documents() -> list[str]:
    col = get_collection()
    total = col.count()
    if total == 0:
        return []
    results = col.get(include=["metadatas"], limit=total)
    seen: set[str] = set()
    for meta in results["metadatas"]:
        doc_id = meta.get("document_id")
        if doc_id:
            seen.add(doc_id)
    return sorted(seen)
