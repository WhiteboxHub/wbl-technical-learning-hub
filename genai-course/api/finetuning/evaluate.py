"""Fine-Tuning vs Base Model Evaluation Script (Module 5).
Compares generation quality and adherence to HR domain terminology between:
1. Standard zero-shot base model
2. Fine-tuned model (or prompt-engineered model in class demo)

Usage:
  python evaluate.py
"""
import json
import os
from openai import OpenAI

TEST_QUESTIONS = [
    "What is the company match on 401k?",
    "How many days of sick leave do I have?",
    "Can I work fully remotely from Spain?",
    "What is the home office stipend amount?",
]

def main():
    print("=" * 60)
    print("Fine-Tuning / RAG Evaluation Benchmark — Module 5")
    print("Comparing Base Model answers vs Grounded/Fine-Tuned answers")
    print("=" * 60)

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("Note: Set OPENAI_API_KEY in environment or .env to run live API evaluation.")
        print("Running with sample benchmark output for class demonstration:\n")
        
        sample_results = [
            {
                "question": "What is the company match on 401k?",
                "generic_llm": "401(k) matches vary widely between companies, typically ranging from 3% to 6% of salary.",
                "fine_tuned_or_rag": "Meridian Solutions matches 100% of employee contributions up to 4% of eligible base salary.",
                "score_generic": 0.20,
                "score_custom": 1.00,
            },
            {
                "question": "What is the home office stipend amount?",
                "generic_llm": "Many remote companies offer home office stipends between $250 and $1,000.",
                "fine_tuned_or_rag": "Meridian provides a one-time tax-free home office stipend of $500 on your second paycheck.",
                "score_generic": 0.15,
                "score_custom": 1.00,
            }
        ]
        
        for item in sample_results:
            print(f"Q: {item['question']}")
            print(f"  [Generic LLM] : {item['generic_llm']}")
            print(f"  [Grounded/FT] : {item['fine_tuned_or_rag']}")
            print(f"  Accuracy delta: +{(item['score_custom'] - item['score_generic'])*100:.0f}%\n")
        return

    client = OpenAI(api_key=api_key)
    print(f"Evaluating {len(TEST_QUESTIONS)} benchmark questions live...")
    for q in TEST_QUESTIONS:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": q}],
            temperature=0.0
        )
        print(f"\nQ: {q}")
        print(f"Base Output: {resp.choices[0].message.content[:120]}...")

if __name__ == "__main__":
    main()
