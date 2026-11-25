"""In-memory Vector Store and RAG Retriever with Tenant Isolation and Grounding."""
import math
from typing import List, Dict, Any, Optional, Tuple
from claimflow.core.llm import get_llm_provider
from claimflow.data.healthcare_kb import POLICY_GUIDELINES

class VectorDocument(Dict[str, Any]):
    id: str
    content: str
    citation: str
    metadata: Dict[str, Any]
    vector: List[float]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)

class HealthcareVectorStore:
    """Vector database implementation with chunking, metadata filtering, and cosine search."""
    
    def __init__(self):
        self.documents: List[Dict[str, Any]] = []
        self.llm = get_llm_provider()
        self._populate_kb()

    def _populate_kb(self):
        for policy in POLICY_GUIDELINES:
            vec = self.llm.embed(policy["content"] + " " + policy["title"])
            self.documents.append({
                "id": policy["id"],
                "policy_code": policy["policy_code"],
                "title": policy["title"],
                "content": policy["content"],
                "citation": policy["citation"],
                "tenant_id": policy["tenant_id"],
                "vector": vec
            })

    def search(
        self,
        query: str,
        tenant_id: str = "tenant-health-corp",
        top_k: int = 2,
        similarity_threshold: float = 0.40
    ) -> List[Dict[str, Any]]:
        """Retrieves top matching documents strictly matching tenant_id."""
        q_vec = self.llm.embed(query)
        scored: List[Tuple[float, Dict[str, Any]]] = []
        
        for doc in self.documents:
            # Tenant isolation enforcement
            if doc["tenant_id"] != tenant_id:
                continue
            sim = cosine_similarity(q_vec, doc["vector"])
            if sim >= similarity_threshold:
                scored.append((sim, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for score, doc in scored[:top_k]]

_vector_store_instance = None

def get_vector_store() -> HealthcareVectorStore:
    global _vector_store_instance
    if _vector_store_instance is None:
        _vector_store_instance = HealthcareVectorStore()
    return _vector_store_instance
