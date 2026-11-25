"""Pytest test suite for GenAI RAG API.
Covers tokenization, chunking, embeddings, retrieval, generation, and abstention.
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

from app.main import app
from app import tokenizer, chunker

client = TestClient(app)


def test_health_endpoint():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "ok"
    assert "chroma" in data
    assert "openai" in data


def test_tokenize_basic():
    res = client.post("/tokenize", json={"text": "Meridian Solutions provides cloud software."})
    assert res.status_code == 200
    data = res.json()
    assert data["token_count"] > 0
    assert len(data["tokens"]) == data["token_count"]
    assert len(data["words"]) == data["token_count"]
    assert data["truncated"] is False


def test_tokenize_truncation_warning():
    # Model with small context limit for test
    sample_text = "word " * 1000
    tokens = tokenizer.tokenize(sample_text, model="text-embedding-3-small")
    assert tokens["token_count"] > 0
    assert tokens["context_limit"] == 8191


def test_chunking_fixed():
    text = "Sentence one. Sentence two. Sentence three. Sentence four. Sentence five."
    res = client.post("/chunk", json={
        "text": text,
        "strategy": "fixed",
        "chunk_size": 4,
        "chunk_overlap": 1
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_chunks"] >= 1
    assert "chunks" in data
    for c in data["chunks"]:
        assert "text" in c
        assert "token_count" in c


def test_chunking_recursive():
    sample_text = """# Policy Document
This is section 1 covering employee benefits and 401k plans.
All full time employees are eligible.

This is section 2 covering paid time off and vacation days.
Accrual is 15 days per year."""
    res = client.post("/chunk", json={
        "text": sample_text,
        "strategy": "recursive",
        "chunk_size": 20,
        "chunk_overlap": 5
    })
    assert res.status_code == 200
    data = res.json()
    assert data["total_chunks"] >= 1
    assert data["strategy"] == "recursive"


def test_chunking_invalid_strategy():
    res = client.post("/chunk", json={"text": "Hello", "strategy": "invalid_strategy"})
    assert res.status_code == 422


@patch("app.embeddings._openai")
def test_embed_mocked(mock_openai):
    # Mock OpenAI embeddings call
    mock_data = MagicMock()
    mock_data.embedding = [0.1] * 1536
    mock_resp = MagicMock()
    mock_resp.data = [mock_data]
    mock_openai.return_value.embeddings.create.return_value = mock_resp

    res = client.post("/embed", json={"texts": ["How much PTO do I get?"]})
    assert res.status_code == 200
    data = res.json()
    assert data["dimensions"] == 1536
    assert len(data["embeddings"]) == 1
    assert len(data["embeddings"][0]) == 1536


def test_embed_empty_texts():
    res = client.post("/embed", json={"texts": []})
    assert res.status_code == 422


@patch("app.rag.vq")
@patch("app.rag.embed")
@patch("app.rag._openai")
def test_generate_grounded(mock_openai, mock_embed, mock_vq):
    # Mock embed
    mock_embed.return_value = [[0.1] * 1536]
    # Mock vector search returning relevant chunk
    mock_vq.return_value = [{
        "text": "Meridian provides 15 days of PTO for 0 to 2 years of service.",
        "score": 0.88,
        "document_id": "pto-and-leave-policy",
        "metadata": {"document_id": "pto-and-leave-policy"}
    }]
    # Mock LLM generation
    mock_msg = MagicMock()
    mock_msg.content = "According to [1], employees with 0-2 years get 15 days of PTO."
    mock_choice = MagicMock()
    mock_choice.message = mock_msg
    mock_resp = MagicMock()
    mock_resp.choices = [mock_choice]
    mock_openai.return_value.chat.completions.create.return_value = mock_resp

    res = client.post("/generate", json={"query": "How many PTO days for new hires?"})
    assert res.status_code == 200
    data = res.json()
    assert data["abstained"] is False
    assert "pto-and-leave-policy" in data["sources"]
    assert "[1]" in data["answer"]


@patch("app.rag.vq")
@patch("app.rag.embed")
def test_generate_abstention_on_low_score(mock_embed, mock_vq):
    mock_embed.return_value = [[0.1] * 1536]
    # Similarity score 0.15 is below 0.30 threshold
    mock_vq.return_value = [{
        "text": "Irrelevant text about gardening.",
        "score": 0.15,
        "document_id": "general",
        "metadata": {}
    }]

    res = client.post("/generate", json={"query": "What is the capital of Mars?"})
    assert res.status_code == 200
    data = res.json()
    assert data["abstained"] is True
    assert "cannot find information" in data["answer"].lower()
    assert data["sources"] == []
