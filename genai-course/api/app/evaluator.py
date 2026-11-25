"""LLM-as-judge evaluator — Module 5 demos."""
import json
import os
from openai import OpenAI

_client: OpenAI | None = None


def _openai() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


JUDGE_SYSTEM = """You are an impartial evaluator of RAG (Retrieval-Augmented Generation) answers.
Given a question, an answer, and the context passages that were retrieved, score the answer on two dimensions.

Return ONLY valid JSON in this exact format:
{
  "faithfulness": <float 0.0-1.0>,
  "relevance": <float 0.0-1.0>,
  "reasoning": "<one sentence explanation>"
}

Definitions:
- faithfulness (0.0-1.0): Is every claim in the answer supported by the provided context?
  1.0 = fully grounded, 0.0 = completely fabricated or contradicts context.
- relevance (0.0-1.0): Does the answer actually address the question?
  1.0 = directly and completely, 0.0 = off-topic or empty.
"""


def evaluate(question: str, answer: str, contexts: list[str]) -> dict:
    context_text = "\n\n".join(f"[{i+1}] {c}" for i, c in enumerate(contexts))
    user_msg = (
        f"QUESTION: {question}\n\n"
        f"ANSWER: {answer}\n\n"
        f"CONTEXT:\n{context_text}"
    )
    model = os.getenv("LLM_MODEL", "gpt-4o-mini")
    response = _openai().chat.completions.create(
        model=model,
        temperature=0.0,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM},
            {"role": "user", "content": user_msg},
        ],
    )
    raw = response.choices[0].message.content
    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        result = {"faithfulness": 0.0, "relevance": 0.0,
                  "reasoning": f"Judge returned invalid JSON: {raw[:100]}"}
    return {
        "faithfulness": float(result.get("faithfulness", 0.0)),
        "relevance": float(result.get("relevance", 0.0)),
        "reasoning": result.get("reasoning", ""),
    }
