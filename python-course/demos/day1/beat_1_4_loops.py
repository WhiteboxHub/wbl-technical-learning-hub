"""Day 1, Beat 1.4: Loops: Stirring the Pot (for and while loops)."""

print("=== Beat 1.4: Loops (for & while) ===")

responses = [
    "AI summary ready.",
    "",
    "Translation complete.",
    "ERROR: timeout",
]

print("--- Processing AI responses (for loop) ---")
for index, reply in enumerate(responses, start=1):
    if reply == "":
        print("[skipped empty response]")
        continue
    print(f"[{index}] Processed: {reply}")

print("\n--- Retrying model call (while loop) ---")
attempt = 1
max_attempts = 3
while attempt <= max_attempts:
    if attempt == 2:
        print(f"Attempt {attempt}: Model ready! Stopping retries.")
        break
    print(f"Attempt {attempt}: waiting...")
    attempt += 1

