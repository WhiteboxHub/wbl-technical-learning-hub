"""Day 2, Beat 2.4 (OOP): Constructor (__init__)."""


class AIModel:
    def __init__(self, name, temperature):
        print(f"[__init__ called] Setting up {name}...")
        self.name = name
        self.temperature = temperature


print("=== Beat 2.4: Constructor (__init__) ===")
fast_model = AIModel("gpt-4o-mini", 0.2)
creative_model = AIModel("gemini-2.5-flash", 0.9)

print(f"Model 1: name={fast_model.name}, temp={fast_model.temperature}")
print(f"Model 2: name={creative_model.name}, temp={creative_model.temperature}")

