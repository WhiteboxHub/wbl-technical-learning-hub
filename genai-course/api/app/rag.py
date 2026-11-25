"""RAG pipeline — Module 4 demos.

Pipeline:
  1. Embed the query
  2. Retrieve top-n chunks from ChromaDB
  3. Abstain if no chunk exceeds the similarity threshold
  4. Build system prompt with numbered context blocks
  5. Call OpenAI chat completion (cite [1], [2], [3] in the answer)
  6. Return answer, sources, retrieved chunks, and abstained flag
"""
import os
from openai import OpenAI
from .embeddings import embed
from .vector_store import query as vq

ABSTENTION_THRESHOLD = 0.30  # scores below this → abstain
ABSTENTION_MSG = (
    "I cannot find information about this topic in the Meridian Solutions HR documents. "
    "Please contact HR directly at hr@meridian.com."
)

_client: OpenAI | None = None


def _openai() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def retrieve_and_generate(query: str, n_results: int = 3,
                           temperature: float = 0.2) -> dict:
    abstention_disabled = os.getenv("ABSTENTION_DISABLED", "0") == "1"

    # 1. Embed the query
    query_vec = embed([query])[0]

    # 2. Retrieve
    results = vq(query_vec, n_results, None)

    # 3. Abstention check
    top_score = results[0]["score"] if results else 0.0
    if not abstention_disabled and top_score < ABSTENTION_THRESHOLD:
        return {
            "answer": ABSTENTION_MSG,
            "sources": [],
            "retrieved_chunks": results,
            "abstained": True,
            "top_score": top_score,
        }

    # 4. Build context
    context_blocks = "\n\n".join(
        f"[{i+1}] (source: {r['document_id']}, score: {r['score']})\n{r['text']}"
        for i, r in enumerate(results)
    )

    system_prompt = (
        "You are an HR policy assistant for Meridian Solutions. "
        "Answer the employee's question using ONLY the context blocks provided below. "
        "Cite your sources by their block number, e.g. [1], [2]. "
        "If the context does not contain enough information, say so explicitly — "
        "do NOT make up information.\n\n"
        f"CONTEXT:\n{context_blocks}"
    )

    # 5. Generate
    temp_override = os.getenv("TEMPERATURE_OVERRIDE", "")
    effective_temp = float(temp_override) if temp_override else temperature

    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    response = _openai().chat.completions.create(
        model=model,
        temperature=effective_temp,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query},
        ],
    )
    answer = response.choices[0].message.content

    # 6. Extract cited sources
    sources = []
    for i, r in enumerate(results):
        if f"[{i+1}]" in answer:
            sources.append(r["document_id"])

    return {
        "answer": answer,
        "sources": list(dict.fromkeys(sources)),  # deduplicated, ordered
        "retrieved_chunks": results,
        "abstained": False,
        "top_score": top_score,
    }
