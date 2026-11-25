# Day 2 Teaching Slides — Python II (The Kitchen's Containers)

Use these slides alongside `course/modules/02-python-ii.md` (Beats 2.1 – 2.9).

---

## Slide 1 — Welcome to Day 2: The Kitchen's Containers
- **Goal:** Organize AI data cleanly, write reusable logic, model AI components with OOP, understand search speed, and persist data to files.
- **Today's 5 Topics:**
  1. Functions (`return` vs `print`)
  2. Data Structures (`list`, `tuple`, `set`, `dict`)
  3. **OOP Fundamentals** (Class & Object, `__init__`, `self`, Attributes & Methods, Inheritance)
  4. Big-O Basics (and Comprehensions)
  5. File Handling

---

## Slide 2 — Recipe Cards: Functions (`def`) (Beat 2.1)
- A **function** packages reusable logic with a name and inputs (parameters):
  ```python
  def calculate_cost(tokens, price_per_1k=0.002):
      return (tokens / 1000) * price_per_1k
  ```
- Define once, call anywhere: `cost = calculate_cost(1500)`.

---

## Slide 3 — `return` vs `print()` (Beat 2.1)
- **`print()`** only displays text on screen for humans; the function gives back **`None`**.
- **`return`** sends the actual value back to your program so you can store or reuse it.
- Rule of thumb: **Compute and `return` inside functions; `print` at the end.**

---

## Slide 4 — The Four Containers: `list` & `tuple` (Beat 2.2)
- **`list` `[...]`** — Ordered, **changeable**. Great for multiple AI responses:
  ```python
  responses = ["Summary A", "Summary B"]
  responses.append("Summary C")
  ```
- **`tuple` `(...)`** — Ordered, **fixed (immutable)**. Great for settings that must not change accidentally:
  ```python
  model_spec = ("openai", "gpt-4o-mini")
  ```

---

## Slide 5 — The Four Containers: `set` & `dict` (Beat 2.2)
- **`set` `{...}`** — **Unique** items, unordered, instant lookup. Great for deduplicating tags or stop words:
  ```python
  tags = {"ai", "python", "ai"}  # -> {"ai", "python"}
  ```
- **`dict` `{key: value}`** — Labelled key-value pairs. Great for API payloads & configs:
  ```python
  payload = {"model": "gpt-4o-mini", "temperature": 0.2}
  ```

---

## Slide 6 — Container Comparison Cheat Sheet (Beat 2.2)
| Container | Syntax | Ordered? | Mutable? | Duplicates? | AI Use Case |
|---|---|---|---|---|---|
| `list` | `[a, b]` | Yes | Yes | Yes | Batch of prompts/responses |
| `tuple` | `(a, b)` | Yes | No | Yes | Fixed `(provider, model)` pair |
| `set` | `{a, b}` | No | Yes | **No** | Unique tags / stop words |
| `dict` | `{k: v}` | Insertion | Yes | Keys unique | JSON API request/response |

---

## Slide 7 — OOP: Class and Object (Beat 2.3)
- A **class** is a blueprint; an **object** is a real item built from that blueprint:
  ```python
  class AIModel:
      provider = "local-demo"

  fast_model = AIModel()
  smart_model = AIModel()
  ```
- One class (`AIModel`), many independent objects (`fast_model is smart_model` → `False`).

---

## Slide 8 — Why OOP in AI Engineering? (Beat 2.3)
- Keeps related **settings** (model name, temperature) and **actions** (`generate_response()`) bundled in one place.
- Instead of juggling loose variables and dictionaries, each model configuration becomes its own clean object.

---

## Slide 9 — OOP: Constructor (`__init__`) (Beat 2.4)
- `__init__` runs **automatically** every time you create a new object:
  ```python
  class AIModel:
      def __init__(self, name, temperature):
          self.name = name
          self.temperature = temperature

  fast_model = AIModel("gpt-4o-mini", 0.2)
  ```
- Two underscores on each side (`__init__`); never called directly.

---

## Slide 10 — OOP: The `self` Keyword (Beat 2.5)
- `self` means **"this specific object right here"**.
- Python passes `self` automatically as the first argument when calling a method:
  ```python
  class AIModel:
      def show_config(self):
          print(self.name, self.temperature)

  summary_model.show_config()  # Python passes summary_model as self
  ```

---

## Slide 11 — OOP: Attributes and Methods (Beat 2.6)
- **Attributes** = data stored on an object (nouns, no `()`): `self.name`, `self.call_count`.
- **Methods** = functions inside a class (verbs, called with `()`):
  ```python
  def generate_response(self, prompt):
      self.call_count += 1
      return f"[{self.name}] Simulated answer to: '{prompt}'"
  ```

---

## Slide 12 — OOP: Inheritance (Beat 2.7)
- A **child class** reuses attributes and methods from a **parent class**:
  ```python
  class ChatModel(AIModel):
      def set_system_prompt(self, system_prompt):
          self.system_prompt = system_prompt

      def chat(self, user_message):
          return self.generate_response(f"System({self.system_prompt}) -> {user_message}")
  ```

---

## Slide 13 — Inheritance Recap (Beat 2.7)
- Parent class: `AIModel` (general settings + `generate_response`).
- Child class: `ChatModel(AIModel)` (automatically gets `name`, `temperature`, `generate_response`, plus adds `chat`).
- Write shared logic once in the parent, reuse it in specialized children.

---

## Slide 14 — Comprehensions: Clean Dataset Transforms (Beat 2.8)
- Transform or filter a collection in one readable line:
  ```python
  raw = ["  Summarize AI ", "Explain BIG-O  ", ""]
  clean = [p.strip().lower() for p in raw if p.strip()]
  lengths = {p: len(p) for p in clean}
  ```
- Pattern: `[expression for item in collection if condition]`.

---

## Slide 15 — Big-O Basics: How Speed Scales (Beat 2.8)
- **Big-O** tells us how steps grow as data size `n` grows:
  - **`O(1)` Constant:** Instant lookup (1 step), e.g., `key in my_dict` or `item in my_set`.
  - **`O(n)` Linear:** Checks items one by one, e.g., `item in my_list` or a single `for` loop.
  - **`O(n^2)` Quadratic:** Nested loops comparing every pair (`for a in items: for b in items:`).

---

## Slide 16 — Big-O in Practice: `list` vs `set` (Beat 2.8)
- Checking if a word is in a 50,000-word list (`O(n)`) inside a loop makes your code `O(n^2)` slow.
- Convert the lookup table to a `set` or `dict` (`O(1)`) once—lookups become practically instant!

---

## Slide 17 — Kitchen Logbook: Reading Text Files (Beat 2.9)
- Variables vanish when a script ends; **files** persist on disk.
- Always use `with open(...) as f:` so Python closes the file automatically:
  ```python
  with open("demos/day2/data/prompt_docs.txt", "r", encoding="utf-8") as f:
      lines = [line.strip() for line in f if line.strip()]
  ```

---

## Slide 18 — Working with JSON Configs (Beat 2.9)
- Built-in `json` module maps JSON files straight to Python `dict`/`list`:
  ```python
  import json
  with open("demos/day2/data/model_config.json", "r", encoding="utf-8") as f:
      config = json.load(f)
  ```
- Save a `dict` back to disk: `json.dump(config, f, indent=2)`.

---

## Slide 19 — File Modes & Day 2 Exercise (Beat 2.9)
- Know the 3 main modes:
  - `"r"` = **Read** (default; error if file missing)
  - `"w"` = **Write** (creates file or **overwrites** existing content!)
  - `"a"` = **Append** (adds to the end—use this for logs!)
- **Next:** Complete [exercises/day2_exercise.py](../../exercises/day2_exercise.py).

