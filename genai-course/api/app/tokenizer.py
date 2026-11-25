"""Tokenization helpers for Module 1 demos."""
import os
import tiktoken

CONTEXT_LIMITS: dict[str, int] = {
    "gpt-4o-mini": 128_000,
    "gpt-4o": 128_000,
    "gpt-4": 8_192,
    "gpt-3.5-turbo": 16_385,
    "text-embedding-3-small": 8_191,
    "text-embedding-3-large": 8_191,
}

_WARN_THRESHOLD = 0.9  # warn when token_count > 90% of context limit


def _get_encoding(model: str) -> tiktoken.Encoding:
    try:
        return tiktoken.encoding_for_model(model)
    except KeyError:
        return tiktoken.get_encoding("cl100k_base")


def tokenize(text: str, model: str = "gpt-4o-mini") -> dict:
    enc = _get_encoding(model)
    token_ids = enc.encode(text)
    token_count = len(token_ids)
    context_limit = CONTEXT_LIMITS.get(model, 128_000)
    truncated = token_count > context_limit * _WARN_THRESHOLD
    # Decode each token back to its string representation (shows subword splits)
    words = [enc.decode([t]) for t in token_ids]
    return {
        "tokens": token_ids,
        "token_count": token_count,
        "words": words,
        "truncated": truncated,
        "context_limit": context_limit,
        "model": model,
    }
