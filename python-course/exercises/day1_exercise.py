"""Day 1 Practical Exercise: AI Token Budget Checker.

Complete the TODOs below using Day 1 concepts:
- Variables & Data Types (str, int)
- Input & Type Casting (int(input(...)))
- Loops (for loop with continue and break)
"""

model_name = "gpt-4o-mini"
budget_tokens = 500


def main():
    print(f"=== AI Token Budget Checker ({model_name}) ===")
    print(f"Total token budget: {budget_tokens}")

    # TODO 1: Replace the fixed count below with int(input("How many prompts to test? "))
    prompt_count = 3

    # Sample token estimates for quick testing (replace with input() inside the loop if desired)
    sample_estimates = [120, 0, 250]

    used_tokens = 0
    for i in range(prompt_count):
        # TODO 2: Ask the user with int(input(f"Prompt {i + 1} tokens: "))
        tokens = sample_estimates[i] if i < len(sample_estimates) else 100

        if tokens == 0:
            print(f"Prompt {i + 1}: 0 tokens -> skipped")
            continue

        if used_tokens + tokens > budget_tokens:
            print(f"Prompt {i + 1}: {tokens} tokens would exceed budget! Stopping.")
            break

        used_tokens += tokens
        print(f"Prompt {i + 1}: added {tokens} tokens (running total = {used_tokens})")

    print(f"Final tokens used: {used_tokens} | Remaining budget: {budget_tokens - used_tokens}")


if __name__ == "__main__":
    main()

