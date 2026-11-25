"""Day 2 Practical Exercise: Model Config & Prompt Analyzer.

Complete the TODOs below using Day 2 concepts:
- Functions with return
- Containers (list, set, dict)
- OOP Fundamentals (AIModel class, __init__, self, attributes & methods)
- Comprehensions
- File Handling (with open + json.load)
"""

import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "demos" / "day2" / "data" / "model_config.json"


def analyze_prompts(prompts):
    """Clean prompts, count unique items, and return a summary dict."""
    # TODO 1: Clean prompts with a list comprehension (strip whitespace and lowercase, skip empty)
    cleaned = [p.strip().lower() for p in prompts if p.strip()]

    # TODO 2: Build a set of unique cleaned prompts
    unique_prompts = set(cleaned)

    # TODO 3: Return a dictionary with total_count, unique_count, and cleaned
    return {
        "total_count": len(cleaned),
        "unique_count": len(unique_prompts),
        "cleaned": cleaned,
    }


class AIModel:
    """Simple AIModel class representing a loaded model configuration."""

    def __init__(self, name, temperature):
        # TODO 4: Store name and temperature on self
        self.name = name
        self.temperature = temperature

    def generate_response(self, prompt):
        # TODO 5: Return a simulated response using self.name and self.temperature
        return f"[{self.name} | temp={self.temperature}] Processed: {prompt}"


def main():
    raw_prompts = ["  Summarize notes ", "explain big-o", "SUMMARIZE NOTES", ""]

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        config = json.load(f)

    summary = analyze_prompts(raw_prompts)
    model = AIModel(config["model"], config["temperature"])

    print("=== Model Config & Prompt Analyzer ===")
    print("Model  :", model.name)
    print("Summary:", summary)
    print("Sample :", model.generate_response(summary["cleaned"][0]))


if __name__ == "__main__":
    main()

