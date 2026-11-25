# Day 1 Teaching Slides — Python I (The Labelled Pantry)

Use these slides alongside `course/modules/01-python-i.md` (Beats 1.1 – 1.5).

---

## Slide 1 — Welcome to Day 1: The Labelled Pantry
- **Goal:** Learn the building blocks of Python using an **AI Engineering Kitchen** theme.
- **Today's 5 Topics:**
  1. Python Introduction & Setup
  2. Variables
  3. Data Types
  4. Input & Type Casting
  5. Loops (`for` and `while`)

---

## Slide 2 — Python Introduction & Setup (Beat 1.1)
- Python is an **interpreted** language: `python3` runs your `.py` file line by line from top to bottom.
- Check your setup anytime in the terminal:
  ```bash
  python3 --version
  ```
- Why Python for AI Engineering? Simple syntax, fast to experiment with prompts, data, and model settings.

---

## Slide 3 — Pantry Jars & Variables (Beat 1.1)
- A **variable** is a **labelled jar** holding a value in memory.
- `=` means **assign** (put the value into the jar), not math equals.
- Good naming (`snake_case`):
  ```python
  model_name = "gpt-4o-mini"
  system_prompt = "You are a helpful AI tutor."
  model_name = "gemini-2.5-flash"  # swap what is inside the jar
  ```

---

## Slide 4 — Core Data Types (Beat 1.2)
| Type | Meaning | AI Engineering Example |
|---|---|---|
| `str` | Text inside quotes | `"Summarize this article"` |
| `int` | Whole number | `150` (tokens) |
| `float` | Decimal number | `0.7` (temperature) |
| `bool` | `True` or `False` switch | `True` (stream mode) |
| `NoneType` | Empty / no value yet | `None` (no error yet) |

---

## Slide 5 — Checking Types with `type()` (Beat 1.2)
- Ask Python what is inside any jar:
  ```python
  print(type("gpt-4o-mini"))  # <class 'str'>
  print(type(150))            # <class 'int'>
  print(type(0.7))            # <class 'float'>
  print(type(True))           # <class 'bool'>
  print(type(None))           # <class 'NoneType'>
  ```
- Remember: `"150"` in quotes is `str` (text), NOT `int` (number).

---

## Slide 6 — Reading User Input (Beat 1.3)
- `input("Prompt: ")` pauses and waits for the user to type and press Enter.
- **THE TEXT TRAP:** `input()` **always returns a `str`**, even when the user types digits!
  ```python
  raw_tokens = input("Max tokens: ")  # user types 200 -> "200" (str!)
  print(raw_tokens * 2)               # prints "200200", NOT 400!
  ```

---

## Slide 7 — Fixing the Trap with Type Casting (Beat 1.3)
- Convert text into numbers immediately:
  - `int("200")` → `200` (whole number)
  - `float("0.4")` → `0.4` (decimal number)
  - `str(200)` → `"200"` (text)
- Safe pattern:
  ```python
  max_tokens = int(input("Max tokens: "))
  temperature = float(input("Temperature: "))
  ```

---

## Slide 8 — `for` Loops: Stirring Through Items (Beat 1.4)
- Use a **`for` loop** when you have a sequence of items or a known number of steps:
  ```python
  responses = ["AI summary ready.", "", "Translation complete."]
  for reply in responses:
      if reply == "":
          continue  # skip blank reply
      print("Processed:", reply)
  ```
- `range(1, 4)` generates `1, 2, 3`.

---

## Slide 9 — `while` Loops & Loop Controls (Beat 1.4)
- Use a **`while` loop** to repeat **until a condition becomes `False`** (e.g., API retries):
  ```python
  attempt = 1
  while attempt <= 3:
      if attempt == 2:
          break  # stop the loop early
      attempt += 1
  ```
- `continue` = skip this turn · `break` = exit loop immediately.
- Always update your loop condition so it does not run forever!

---

## Slide 10 — Day 1 Revision & Exercise (Beat 1.5)
- Putting it all together: **AI Prompt Batch Runner**
  1. Store model & token cost in variables (`str`, `int`)
  2. Read task & run count with `input()` + `int()`
  3. Repeat runs with `for step in range(1, runs + 1):`
  4. Accumulate total tokens
- **Next:** Complete [exercises/day1_exercise.py](../../exercises/day1_exercise.py).

