"""Embedding generation using OpenAI — Module 3 demos."""
import math
import os
from openai import OpenAI

_client: OpenAI | None = None


def _openai() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def embed(texts: list[str]) -> list[list[float]]:
    model = os.getenv("EMBED_MODEL", "text-embedding-3-small")
    response = _openai().embeddings.create(input=texts, model=model)
    return [item.embedding for item in response.data]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    mag_a = math.sqrt(sum(x ** 2 for x in a))
    mag_b = math.sqrt(sum(x ** 2 for x in b))
    if mag_a == 0 or mag_b == 0:
        return 0.0
    return dot / (mag_a * mag_b)
