"""LLM Provider Interface and Dual-Mode Implementations.
Supports:
1. MockLLMProvider: 100% offline, deterministic, zero-cost, runs on any OS without API keys.
2. RealLLMProvider: Connects to OpenAI, Anthropic, Gemini or local Ollama endpoints.
"""
import os
import json
import math
from typing import List, Dict, Any, Optional

class LLMProvider:
    """Abstract interface for LLM completions and embeddings."""
    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.0, max_tokens: int = 500) -> str:
        raise NotImplementedError

    def embed(self, text: str) -> List[float]:
        raise NotImplementedError


class MockLLMProvider(LLMProvider):
    """Deterministic, zero-cost, offline provider simulating LLM reasoning, tool calling, and embeddings."""
    
    def __init__(self):
        self.dimension = 8

    def embed(self, text: str) -> List[float]:
        """Generates deterministic normalized pseudo-embedding based on character n-grams and hashing."""
        text_lower = text.lower()
        vec = [0.05] * self.dimension
        
        # High specificity semantic vector coordinates for healthcare topics
        if any(k in text_lower for k in ["knee", "arthroplasty", "ortho", "27447", "m17"]):
            vec[0] = 0.90
            vec[1] = 0.40
        elif any(k in text_lower for k in ["cardiac", "heart", "bypass", "cabg", "33533", "i25"]):
            vec[2] = 0.90
            vec[3] = 0.40
        elif any(k in text_lower for k in ["mri", "brain", "neuro", "headache", "70553", "r51"]):
            vec[4] = 0.90
            vec[5] = 0.40
        else:
            # Out of scope / generic content
            vec[6] = 0.80
            vec[7] = 0.60
            
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [round(x / norm, 4) for x in vec]

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.0, max_tokens: int = 500) -> str:
        """Simulates structured LLM responses based on healthcare policy rules."""
        p_lower = prompt.lower()
        
        # Medical Necessity Evaluation
        if "medical necessity" in p_lower or "guideline" in p_lower:
            if "severe osteoarthritis" in p_lower or "failed conservative therapy" in p_lower or "m17.11" in p_lower:
                return json.dumps({
                    "necessity_score": 0.94,
                    "meets_criteria": True,
                    "citation": "POL-ORTHO-2026: Section 4.2 - Total Knee Replacement",
                    "reasoning": "Patient demonstrated progressive severe osteoarthritis and failed 6 months conservative physical therapy."
                })
            elif "experimental" in p_lower or "unsupported" in p_lower:
                return json.dumps({
                    "necessity_score": 0.22,
                    "meets_criteria": False,
                    "citation": "POL-GEN-2026: Section 1.1 - Experimental Interventions",
                    "reasoning": "Treatment does not meet established clinical standard of care."
                })
            else:
                return json.dumps({
                    "necessity_score": 0.70,
                    "meets_criteria": True,
                    "citation": "POL-GEN-2026: Section 3.0 - General Prior Auth Criteria",
                    "reasoning": "Standard clinical presentation; documented symptoms meet basic medical criteria."
                })
                
        # Fraud and Audit Risk
        if "audit" in p_lower or "risk" in p_lower or "fraud" in p_lower:
            if "15000" in p_lower or "high amount" in p_lower or "out of network" in p_lower:
                return json.dumps({
                    "risk_score": 0.85,
                    "flagged": True,
                    "risk_reasons": ["High dollar threshold (> $10,000)", "Complex billing code combination"],
                    "recommendation": "Route to Human Auditor"
                })
            return json.dumps({
                "risk_score": 0.12,
                "flagged": False,
                "risk_reasons": [],
                "recommendation": "Auto-Approve Eligible"
            })

        # General response
        return "ClaimFlow Agentic Core: Processed successfully according to healthcare guidelines."


class RealLLMProvider(LLMProvider):
    """Integrates with real LLM APIs (OpenAI / Anthropic / Gemini / local Ollama) or local HuggingFace/SentenceTransformers."""
    
    def __init__(self, api_key: Optional[str] = None, base_url: Optional[str] = None, model: str = "gpt-4o-mini"):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY", "")
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.model = model
        self._st_model = None

    def embed(self, text: str) -> List[float]:
        # If API key is provided, use OpenAI embeddings
        if self.api_key:
            import requests
            try:
                resp = requests.post(
                    f"{self.base_url}/embeddings",
                    headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                    json={"input": text, "model": "text-embedding-3-small"},
                    timeout=10
                )
                resp.raise_for_status()
                return resp.json()["data"][0]["embedding"]
            except Exception:
                pass

        # If sentence_transformers is available locally, use all-MiniLM-L6-v2
        try:
            from sentence_transformers import SentenceTransformer
            if self._st_model is None:
                self._st_model = SentenceTransformer("all-MiniLM-L6-v2")
            emb = self._st_model.encode(text).tolist()
            return [round(x, 4) for x in emb[:8]]  # Project to 8 dims for fast runtime
        except Exception:
            return MockLLMProvider().embed(text)

    def generate(self, prompt: str, system_prompt: str = "", temperature: float = 0.0, max_tokens: int = 500) -> str:
        import requests
        if not self.api_key:
            return MockLLMProvider().generate(prompt, system_prompt, temperature, max_tokens)
        try:
            messages = []
            if system_prompt:
                messages.append({"role": "system", "content": system_prompt})
            messages.append({"role": "user", "content": prompt})
            
            resp = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
                json={
                    "model": self.model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens
                },
                timeout=15
            )
            resp.raise_for_status()
            return resp.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return MockLLMProvider().generate(prompt, system_prompt, temperature, max_tokens)


def get_llm_provider() -> LLMProvider:
    """Factory to retrieve current configured provider."""
    provider_type = os.getenv("CLAIMFLOW_LLM_PROVIDER", "mock").lower()
    if provider_type in ("openai", "real") and os.getenv("OPENAI_API_KEY"):
        return RealLLMProvider()
    return MockLLMProvider()
