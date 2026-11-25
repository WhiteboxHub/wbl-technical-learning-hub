"""Day 2, Beat 2.1: Recipe Cards (Return vs Print)."""


def print_only_cost(tokens):
    print((tokens / 1000) * 0.002)


def calculate_cost(tokens, price_per_1k=0.002):
    return (tokens / 1000) * price_per_1k


print("=== Beat 2.1: Recipe Cards (Return vs Print) ===")
result_bad = print_only_cost(1500)
result_good = calculate_cost(1500)

print("print_only_cost returned :", result_bad)
print("calculate_cost returned  :", round(result_good, 6))
print("Two API calls total ($)  :", round(result_good * 2, 6))

