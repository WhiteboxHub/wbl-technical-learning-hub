"""Chunking strategies for Module 3 demos.

Three strategies:
  fixed      — split every chunk_size tokens, with chunk_overlap token overlap
  recursive  — LangChain RecursiveCharacterTextSplitter (respects paragraphs → sentences → words)
  sentence   — split on sentence boundaries, merge up to chunk_size tokens
"""
import os
import re
import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter


def _enc():
    return tiktoken.get_encoding("cl100k_base")


def _token_count(text: str) -> int:
    return len(_enc().encode(text))


def _fixed(text: str, chunk_size: int, chunk_overlap: int) -> list[dict]:
    enc = _enc()
    tokens = enc.encode(text)
    chunks = []
    step = max(1, chunk_size - chunk_overlap)
    for start in range(0, len(tokens), step):
        end = min(start + chunk_size, len(tokens))
        chunk_tokens = tokens[start:end]
        chunk_text = enc.decode(chunk_tokens)
        # Approximate char positions
        char_start = len(enc.decode(tokens[:start]))
        char_end = char_start + len(chunk_text)
        chunks.append({
            "text": chunk_text,
            "char_start": char_start,
            "char_end": char_end,
            "token_count": len(chunk_tokens),
        })
        if end == len(tokens):
            break
    return chunks


def _recursive(text: str, chunk_size: int, chunk_overlap: int) -> list[dict]:
    # LangChain splitter works in characters; we set size proportionally
    # Approximate: 1 token ≈ 4 chars for English
    char_size = max(1, chunk_size * 4)
    char_overlap = min(max(0, chunk_overlap * 4), max(0, char_size - 1))
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=char_size,
        chunk_overlap=char_overlap,
        length_function=len,
    )
    raw_chunks = splitter.split_text(text)
    result = []
    pos = 0
    for chunk_text in raw_chunks:
        idx = text.find(chunk_text, pos)
        char_start = idx if idx != -1 else pos
        char_end = char_start + len(chunk_text)
        result.append({
            "text": chunk_text,
            "char_start": char_start,
            "char_end": char_end,
            "token_count": _token_count(chunk_text),
        })
        pos = char_end
    return result


def _sentence(text: str, chunk_size: int, chunk_overlap: int) -> list[dict]:
    # Split on sentence boundaries then merge up to chunk_size tokens
    sentences = re.split(r'(?<=[.!?])\s+', text)
    chunks = []
    current: list[str] = []
    current_tokens = 0
    char_pos = 0

    for sent in sentences:
        sent_tokens = _token_count(sent)
        if current_tokens + sent_tokens > chunk_size and current:
            chunk_text = " ".join(current)
            chunks.append({
                "text": chunk_text,
                "char_start": char_pos - len(chunk_text),
                "char_end": char_pos,
                "token_count": current_tokens,
            })
            # Keep overlap: last sentence carries over
            current = current[-1:] if chunk_overlap > 0 else []
            current_tokens = _token_count(" ".join(current))
        current.append(sent)
        current_tokens += sent_tokens
        char_pos += len(sent) + 1

    if current:
        chunk_text = " ".join(current)
        chunks.append({
            "text": chunk_text,
            "char_start": max(0, char_pos - len(chunk_text)),
            "char_end": char_pos,
            "token_count": current_tokens,
        })
    return chunks


def chunk(text: str, strategy: str = "recursive",
          chunk_size: int = 512, chunk_overlap: int = 64) -> list[dict]:
    # Allow env overrides (break.sh injects CHUNK_SIZE / CHUNK_OVERLAP)
    chunk_size = int(os.getenv("CHUNK_SIZE", chunk_size))
    chunk_overlap = int(os.getenv("CHUNK_OVERLAP", chunk_overlap))

    if strategy == "fixed":
        return _fixed(text, chunk_size, chunk_overlap)
    elif strategy == "sentence":
        return _sentence(text, chunk_size, chunk_overlap)
    else:
        return _recursive(text, chunk_size, chunk_overlap)
