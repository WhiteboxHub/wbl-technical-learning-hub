"""Day 1, Beat 1.3: Input & The Text Trap (input() always returns str)."""

print("=== Beat 1.3: Input & The Text Trap ===")

user_prompt = input("Enter your AI prompt: ")
raw_tokens = input("Max tokens: ")
raw_temp = input("Temperature (0.0-1.0): ")

# The Text Trap: raw_tokens is a str, so * 2 repeats text instead of multiplying!
trapped = raw_tokens * 2

# Type Casting fixes the trap
max_tokens = int(raw_tokens)
temperature = float(raw_temp)

print(f"Prompt received : {user_prompt!r} ({type(user_prompt)})")
print(f"TRAP before cast: raw_tokens * 2 = {trapped!r} ({type(trapped)})")
print(f"SAFE after int(): max_tokens * 2 = {max_tokens * 2} ({type(max_tokens)})")
print(f"Temperature     : {temperature} ({type(temperature)})")

