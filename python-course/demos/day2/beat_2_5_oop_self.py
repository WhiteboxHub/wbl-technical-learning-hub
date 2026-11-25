"""Day 2, Beat 2.5 (OOP): The self Keyword."""


class AIModel:
    def __init__(self, name, temperature):
        self.name = name
        self.temperature = temperature

    def show_config(self):
        # 'self' points to whichever object called this method
        print(f"Config -> model={self.name}, temperature={self.temperature}")


print("=== Beat 2.5: The self Keyword ===")
summary_model = AIModel("gpt-4o-mini", 0.1)
story_model = AIModel("claude-haiku", 0.8)

summary_model.show_config()
story_model.show_config()

