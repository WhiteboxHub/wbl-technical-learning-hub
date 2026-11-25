"""Day 2, Beat 2.2: The Four Containers (list, tuple, set, dict)."""

print("=== Beat 2.2: The Four Containers ===")

responses = ["Summary A", "Summary B", "Summary A"]
model_spec = ("openai", "gpt-4o-mini")
unique_tags = {"ai", "python", "ai"}
api_request = {
    "model": model_spec[1],
    "temperature": 0.2,
    "max_tokens": 150,
}

print("list  (responses)  :", responses)
print("tuple (model_spec) :", model_spec)
print("set   (unique_tags):", sorted(unique_tags), f"(count = {len(unique_tags)})")
print("dict  (api_request):", api_request)

