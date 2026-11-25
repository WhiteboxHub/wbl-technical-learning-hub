"""Day 1, Beat 1.5: Practical Demonstration & Revision (AI Prompt Batch Runner)."""

model_name = "gpt-4o-mini"
tokens_per_call = 120

print("=== Beat 1.5: AI Prompt Batch Runner (Revision) ===")
task = input("Task name: ")
runs = int(input("How many runs? "))

total_tokens = 0
for step in range(1, runs + 1):
    total_tokens += tokens_per_call
    print(f"Run {step}/{runs} on {model_name}: {task!r} -> OK ({tokens_per_call} tokens)")

print("Batch finished. Total tokens used:", total_tokens)

