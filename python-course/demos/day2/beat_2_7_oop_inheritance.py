"""Day 2, Beat 2.7 (OOP): Inheritance (Parent Class and Child Class)."""


class AIModel:
    """Parent class: shared model settings and basic response generation."""

    def __init__(self, name, temperature):
        self.name = name
        self.temperature = temperature

    def generate_response(self, prompt):
        return f"[{self.name} | temp={self.temperature}] {prompt}"


class ChatModel(AIModel):
    """Child class: inherits AIModel attributes and methods, adds chat helper."""

    def set_system_prompt(self, system_prompt):
        self.system_prompt = system_prompt

    def chat(self, user_message):
        combined = f"System({self.system_prompt}) -> User({user_message})"
        return self.generate_response(combined)


print("=== Beat 2.7: Inheritance ===")
bot = ChatModel("gpt-4o-mini", 0.2)
bot.set_system_prompt("Be brief and beginner-friendly")

print("Inherited name :", bot.name)
print("Inherited call :", bot.generate_response("Hello AI"))
print("Child chat call:", bot.chat("What is inheritance?"))

