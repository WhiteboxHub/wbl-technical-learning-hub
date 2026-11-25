"""Shared test fixtures for Unit, Integration, E2E, and Regression tests."""
import os
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Ensure test environment variables
os.environ["TESTING"] = "1"
os.environ["OPENAI_API_KEY"] = "sk-test-key-for-unit-testing-0123456789"
os.environ["CHROMA_HOST"] = "localhost"
os.environ["CHROMA_PORT"] = "8001"
os.environ["EMBED_MODEL"] = "text-embedding-3-small"
os.environ["LLM_MODEL"] = "gpt-4o-mini"


@pytest.fixture
def sample_hr_text():
    return (
        "# Meridian Solutions Paid Time Off Policy\n\n"
        "Full-time employees receive 18 days of paid time off per calendar year.\n"
        "PTO accrues at 1.5 days per month of service.\n"
        "Employees may carry over a maximum of 5 unused days into the next calendar year.\n"
        "Requests must be submitted at least 14 days in advance to the direct manager."
    )


@pytest.fixture
def mock_embedding_1536():
    """Returns a deterministic 1536-dimensional mock embedding vector."""
    vec = [0.0] * 1536
    # Seed with non-zero values for realistic vector operations
    for i in range(1536):
        vec[i] = ((i % 17) - 8) / 10.0
    # Normalize to unit length
    magnitude = sum(x**2 for x in vec) ** 0.5
    return [x / magnitude for x in vec]


@pytest.fixture
def mock_openai_embed(mock_embedding_1536):
    """Mocks openai.embeddings.create call."""
    with patch("app.embeddings._openai") as mock_openai:
        mock_data = MagicMock()
        mock_data.embedding = mock_embedding_1536
        mock_resp = MagicMock()
        mock_resp.data = [mock_data]
        mock_openai.return_value.embeddings.create.return_value = mock_resp
        yield mock_openai


@pytest.fixture
def mock_chroma_collection(mock_embedding_1536):
    """Mocks chromadb collection operations for testing vector store in isolation."""
    mock_col = MagicMock()
    mock_col.count.return_value = 5
    mock_col.query.return_value = {
        "documents": [["Full-time employees receive 18 days of paid time off per calendar year."]],
        "metadatas": [[{"document_id": "pto-and-leave-policy.md", "chunk_index": 0, "token_count": 30}]],
        "distances": [[0.12]],  # cosine distance 0.12 -> similarity 0.88
    }
    with patch("app.vector_store.get_collection", return_value=mock_col):
        yield mock_col


@pytest.fixture
def test_client():
    """FastAPI TestClient with seeded mocked dependencies."""
    from app.main import app
    return TestClient(app)
