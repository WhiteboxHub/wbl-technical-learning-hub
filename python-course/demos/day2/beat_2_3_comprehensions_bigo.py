"""Day 2, Beat 2.3: Comprehensions & Big-O Basics."""

import time

print("=== Beat 2.3: Comprehensions & Big-O ===")

raw_prompts = ["  Summarize AI ", "Explain BIG-O  ", ""]
clean_prompts = [p.strip().lower() for p in raw_prompts if p.strip()]
length_map = {p: len(p) for p in clean_prompts}

print("Clean prompts :", clean_prompts)
print("Length map    :", length_map)

# Big-O benchmark: O(n) list scan vs O(1) set hash lookup
vocab_list = list(range(50_000))
vocab_set = set(vocab_list)
targets = range(49_000, 50_000)

t0 = time.perf_counter()
list_hits = sum(1 for t in targets if t in vocab_list)
t_list_ms = (time.perf_counter() - t0) * 1000

t1 = time.perf_counter()
set_hits = sum(1 for t in targets if t in vocab_set)
t_set_ms = (time.perf_counter() - t1) * 1000

print(f"Big-O check (1,000 lookups in 50,000 items; hits={list_hits}/{set_hits}):")
print(f"  list O(n) scan : {t_list_ms:.2f} ms")
print(f"  set  O(1) hash : {t_set_ms:.4f} ms")

