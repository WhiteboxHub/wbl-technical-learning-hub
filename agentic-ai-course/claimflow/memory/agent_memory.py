"""Agent Memory Architecture: Short-Term Working Memory & Long-Term Episodic Storage."""
from typing import Dict, List, Any, Optional
from datetime import datetime

class AgentMemoryStore:
    """Manages short-term scratchpad memory and long-term provider compliance history."""
    
    def __init__(self):
        # Short-term session memory: session_id -> list of observations
        self.short_term: Dict[str, List[Dict[str, Any]]] = {}
        # Long-term episodic memory: claim_id -> episodic memory record
        self.episodic_memory: Dict[str, Dict[str, Any]] = {}
        # Long-term provider history: provider_id -> historical audit record
        self.long_term_providers: Dict[str, Dict[str, Any]] = {
            "PRV-501": {
                "name": "Metro Surgical Specialists",
                "fraud_rate": 0.01,
                "clean_claims_count": 482,
                "past_violations": 0,
                "status": "trusted"
            },
            "PRV-999": {
                "name": "QuickCare Unlicensed Clinic",
                "fraud_rate": 0.45,
                "clean_claims_count": 8,
                "past_violations": 3,
                "status": "high_scrutiny"
            }
        }

    def record_short_term(self, session_id: str, note: str):
        if session_id not in self.short_term:
            self.short_term[session_id] = []
        self.short_term[session_id].append({
            "timestamp": datetime.utcnow().isoformat(),
            "note": note
        })

    def get_short_term(self, session_id: str) -> List[Dict[str, Any]]:
        return self.short_term.get(session_id, [])

    def store_episodic(self, key: str, record: Dict[str, Any], tenant_id: str = "tenant-health-corp"):
        """Stores a persistent episodic prior-authorization record with tenant isolation."""
        self.episodic_memory[f"{tenant_id}:{key}"] = {
            "record": record,
            "tenant_id": tenant_id,
            "stored_at": datetime.utcnow().isoformat()
        }

    def get_episodic(self, key: str, tenant_id: str = "tenant-health-corp") -> Optional[Dict[str, Any]]:
        """Retrieves a persistent episodic record enforcing tenant isolation."""
        entry = self.episodic_memory.get(f"{tenant_id}:{key}")
        return entry.get("record") if entry else None

    def lookup_provider_profile(self, provider_id: str) -> Optional[Dict[str, Any]]:
        return self.long_term_providers.get(provider_id)

    def update_provider_record(self, provider_id: str, claim_approved: bool):
        if provider_id not in self.long_term_providers:
            self.long_term_providers[provider_id] = {
                "name": f"Provider {provider_id}",
                "fraud_rate": 0.0,
                "clean_claims_count": 0,
                "past_violations": 0,
                "status": "standard"
            }
        rec = self.long_term_providers[provider_id]
        if claim_approved:
            rec["clean_claims_count"] += 1
        else:
            rec["past_violations"] += 1

_memory_store = None

def get_memory_store() -> AgentMemoryStore:
    global _memory_store
    if _memory_store is None:
        _memory_store = AgentMemoryStore()
    return _memory_store
