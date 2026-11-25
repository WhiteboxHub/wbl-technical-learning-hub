"""Day 2, Beat 2.3 (OOP): Class and Object."""


class AIModel:
    """Blueprint for an AI model configuration."""
    provider = "local-demo"


print("=== Beat 2.3: Class and Object ===")
fast_model = AIModel()
smart_model = AIModel()

print("Class blueprint :", AIModel)
print("Object 1        :", type(fast_model), "| provider =", fast_model.provider)
print("Object 2        :", type(smart_model), "| provider =", smart_model.provider)
print("Same object?    :", fast_model is smart_model)

