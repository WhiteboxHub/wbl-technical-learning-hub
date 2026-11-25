"""Day 2, Beat 2.6 (OOP): Attributes and Methods."""


class AIModel:
    def __init__(self, name, temperature):
        # Instance attributes (data stored on this object)
        self.name = name
        self.temperature = temperature
        self.call_count = 0

    # Instance method (action this object can perform)
    def generate_response(self, prompt):
        self.call_count += 1
        return f"[{self.name} | temp={self.temperature}] Simulated answer to: '{prompt}'"


print("=== Beat 2.6: Attributes and Methods ===")
assistant = AIModel("gpt-4o-mini", 0.3)

reply_1 = assistant.generate_response("Explain Python classes")
reply_2 = assistant.generate_response("Summarize Big-O")

print("Reply 1    :", reply_1)
print("Reply 2    :", reply_2)
print("Calls made :", assistant.call_count)

