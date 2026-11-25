# Day 1 — Python I (The Labelled Pantry)

Teach-skill content file. Format is described in `.claude/skills/teach-python-class/SKILL.md`.
Slides: `course/slides/day1-python-i-slides.md` (slide numbers below).
Stack requirements: Python 3.10+ installed (`scripts/setup.sh --day1` must be READY).
Time: about 90 minutes with demos, questions, and exercise.

## Objectives
By the end of Day 1, candidates can check their Python setup, store AI prompts and settings in variables, choose the right basic data types, read and convert user input safely, and process multiple AI responses using `for` and `while` loops.

## Stack requirements
- `python3 --version` reports Python 3.10+.
- Demo files present in `demos/day1/`:
  - `beat_1_1_variables.py`
  - `beat_1_2_data_types.py`
  - `beat_1_3_input_casting.py`
  - `beat_1_4_loops.py`
  - `beat_1_5_revision.py`
- Exercise file: `exercises/day1_exercise.py`.

---

### Beat 1.1 – Pantry Jars & Variables
- **Slides:** Slides 1–3 (`course/slides/day1-python-i-slides.md`)
- **Learning objective:** Verify Python setup, create variables with clear names, and reassign values.
- **Simple technical definition:** A **variable** is a named label attached to a value stored in computer memory so your code can read or update it later. Python is an interpreted language: the `python3` program reads your `.py` file line by line from top to bottom.
- **Say (Instructor talking points):**
  - Before cooking, we check the kitchen works: `python3 --version` confirms Python is installed and ready.
  - Think of variables like **labelled jars in a pantry**: the label on the outside (`model_name`) stays clear while what is inside (`"gpt-4o-mini"`) can be swapped anytime.
  - Use `snake_case` (lowercase words joined by underscores) for readable variable names, and `=` means "store the right side under the left name", not math equality.
- **Real-world AI example:** An AI assistant script stores the active `model_name`, the `system_prompt`, and the `default_temperature` in variables so you can switch models in one place instead of editing 20 lines.
- **Python code example:**
  ```python
  model_name = "gpt-4o-mini"
  system_prompt = "You are a helpful AI tutor."
  print("Active model:", model_name)

  # Swap what is inside the jar
  model_name = "gemini-2.5-flash"
  print("Updated model:", model_name)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 --version
  python3 demos/day1/beat_1_1_variables.py
  ```
  **Point out:** `python3 --version` shows our setup is healthy; running the script prints the initial `gpt-4o-mini` jar value and then prints `gemini-2.5-flash` after reassignment.
- **Expected output:**
  ```text
  === Beat 1.1: Pantry Jars & Variables ===
  System Prompt : You are a helpful AI tutor.
  Active Model  : gpt-4o-mini
  Updated Model : gemini-2.5-flash
  ```
- **Common mistakes:**
  - Starting variable names with a number (`1st_prompt = "hi"` → `SyntaxError`) or using spaces (`model name = "gpt"`).
  - Using quotes around a variable name when printing (`print("model_name")` prints the word `model_name` instead of its value).
- **Ask (Student interaction question):**
  - Q: If `prompt = "Hello"` and on the next line we write `prompt = "Summarize"`, what does `print(prompt)` show and why? — A: It shows `Summarize` because reassigning a variable replaces what is inside that labelled jar.
  - Q: Why is `user_prompt` a better variable name than `x` in an AI app? — A: Descriptive `snake_case` names make it clear what data the variable holds when reading or debugging code later.
- **Done when:** candidates can explain `=` as assignment and verify `python3 --version` works.

---

### Beat 1.2 – Python Data Types
- **Slides:** Slides 4–5 (`course/slides/day1-python-i-slides.md`)
- **Learning objective:** Identify and inspect Python's core data types (`str`, `int`, `float`, `bool`, `NoneType`) using `type()`.
- **Simple technical definition:** A **data type** tells Python what kind of value is stored in a variable and what operations are allowed on it: `str` (text), `int` (whole numbers), `float` (decimal numbers), `bool` (`True`/`False` switches), and `None` (empty / nothing yet).
- **Say (Instructor talking points):**
  - Not all pantry jars hold the same kind of ingredient: text, whole counts, decimals, and on/off switches behave differently.
  - In AI settings, `model_name` is `str`, `max_tokens` is `int`, `temperature` is `float`, `stream` is `bool`, and `error_message` starts as `None`.
  - Use `type(value)` whenever you are unsure what kind of value a variable holds.
- **Real-world AI example:** Every call to an AI model sends typed settings: a string prompt (`"Explain loops"`), an integer token cap (`256`), a decimal creativity temperature (`0.7`), a boolean streaming flag (`True`), and an optional error slot (`None`).
- **Python code example:**
  ```python
  prompt_text = "Explain recursion simply"   # str
  max_tokens = 256                           # int
  temperature = 0.7                          # float
  stream_response = True                     # bool
  api_error = None                           # NoneType

  print(type(prompt_text), type(max_tokens), type(temperature), type(stream_response), type(api_error))
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day1/beat_1_2_data_types.py
  ```
  **Point out:** `150` is an `int`, while `0.7` is a `float`, and `"150"` in quotes would be a `str` (text, not math).
- **Expected output:**
  ```text
  === Beat 1.2: Python Data Types ===
  prompt_text     = 'Explain Python in one sentence' -> <class 'str'>
  max_tokens      = 150 -> <class 'int'>
  temperature     = 0.7 -> <class 'float'>
  stream_response = True -> <class 'bool'>
  api_error       = None -> <class 'NoneType'>
  ```
- **Common mistakes:**
  - Writing `true` or `false` in lowercase instead of `True` / `False` (`NameError`).
  - Wrapping numbers in quotes (`temperature = "0.7"`), turning a number into a `str` so math fails later.
- **Ask (Student interaction question):**
  - Q: What is the difference between `100` and `"100"` in Python? — A: `100` is an `int` (you can do math with it); `"100"` is a `str` (text characters).
  - Q: Which data type should you use for an AI model's `temperature` like `0.2` or `1.0`? — A: `float` (decimal number).
- **Done when:** candidates can match prompt, token count, temperature, and streaming flag to `str`, `int`, `float`, and `bool`.

---

### Beat 1.3 – Input & The Text Trap
- **Slides:** Slides 6–7 (`course/slides/day1-python-i-slides.md`)
- **Learning objective:** Accept user input with `input()` and convert strings to numbers using `int()` and `float()`.
- **Simple technical definition:** `input()` pauses the program, reads what the user types, and **always returns a `str` (text)**—even if the user typed digits. **Type casting** (`int()`, `float()`, `str()`) converts a value from one data type into another.
- **Say (Instructor talking points):**
  - When a user types `200` at a prompt, Python sees `"200"` (text), not the number `200`. That is **The Text Trap**.
  - If you try `"200" + 50` or `"0.7" * 2` without casting, Python either crashes with a `TypeError` or repeats text (`"200" * 2 == "200200"`).
  - Fix the trap right away by wrapping `input()` in `int(...)` for whole numbers or `float(...)` for decimals.
- **Real-world AI example:** An interactive AI CLI asks the user for a prompt (`str`), a max token limit (`int`), and a temperature (`float`). Without casting, calculating estimated cost or remaining tokens crashes.
- **Python code example:**
  ```python
  user_prompt = input("Enter your AI prompt: ")
  raw_tokens = input("Max tokens: ")        # returns str, e.g. "200"
  max_tokens = int(raw_tokens)              # cast str -> int
  temperature = float(input("Temperature (0.0-1.0): "))

  print("Prompt:", user_prompt)
  print("Double token budget:", max_tokens * 2)
  print("Half temperature:", temperature / 2)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  printf "Summarize AI notes\n200\n0.4\n" | python3 demos/day1/beat_1_3_input_casting.py
  ```
  *(Note for live room: run `python3 demos/day1/beat_1_3_input_casting.py` without `printf` if you want to type live at the keyboard.)*
  **Point out:** before casting, `type(raw_tokens)` is `<class 'str'>` and `raw_tokens * 2` prints `"200200"`; after `int(raw_tokens)`, `max_tokens * 2` prints `400`.
- **Expected output:**
  ```text
  === Beat 1.3: Input & The Text Trap ===
  Prompt received : 'Summarize AI notes' (<class 'str'>)
  TRAP before cast: raw_tokens * 2 = '200200' (<class 'str'>)
  SAFE after int(): max_tokens * 2 = 400 (<class 'int'>)
  Temperature     : 0.4 (<class 'float'>)
  ```
- **Common mistakes:**
  - Doing `int("0.7")` instead of `float("0.7")` (`ValueError` because `"0.7"` has a decimal point).
  - Forgetting that `"50" + "50"` joins text into `"5050"` instead of adding to `100`.
- **Ask (Student interaction question):**
  - Q: Why does `input("Tokens: ") + 10` crash with a `TypeError` even if the user types `50`? — A: Because `input()` always returns a `str` (`"50"`), and Python cannot add an `int` (`10`) directly to a `str`.
  - Q: What does `"200" * 2` evaluate to in Python? — A: `"200200"` (repeating the string twice, not multiplying the number).
- **Done when:** candidates can explain why `input()` returns `str` and choose between `int()` and `float()`.

---

### Beat 1.4 – Loops: Stirring the Pot
- **Slides:** Slides 8–9 (`course/slides/day1-python-i-slides.md`)
- **Learning objective:** Repeat actions over a collection with `for` loops and until a condition changes with `while` loops, using `break` and `continue`.
- **Simple technical definition:** A **`for` loop** runs once for every item in a known sequence (like a list of AI responses). A **`while` loop** keeps repeating as long as a condition remains `True` (like retrying a failed API call until it succeeds or hits a limit).
- **Say (Instructor talking points):**
  - Instead of copy-pasting the same `print()` or processing line 10 times, a loop stirs through every item automatically.
  - Use **`for`** when you know the items or count ahead of time (e.g. `for response in responses:` or `for i in range(3):`).
  - Use **`while`** when you do not know how many tries it will take—for example, polling or retrying until `retries == 3` or `status == "ok"`. Always make sure the condition eventually becomes `False` so you don't create an infinite loop!
  - `continue` skips the rest of the current turn; `break` exits the loop immediately.
- **Real-world AI example:** Processing a batch of AI model responses: skip empty responses (`continue`), count valid answers with a `for` loop, and simulate a `while` loop that retries a rate-limited request up to 3 attempts or stops early (`break`) once `"OK"` arrives.
- **Python code example:**
  ```python
  responses = ["AI summary ready.", "", "Translation complete.", "ERROR: timeout"]

  for reply in responses:
      if reply == "":
          continue  # skip blank reply
      print("Processed:", reply)

  attempt = 1
  while attempt <= 3:
      print("Checking model status, attempt", attempt)
      if attempt == 2:
          print("Model ready!")
          break
      attempt += 1
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day1/beat_1_4_loops.py
  ```
  **Point out:** the `for` loop skips the empty string with `continue`; the `while` loop increments `attempt` each turn and stops at attempt 2 via `break` instead of running forever.
- **Expected output:**
  ```text
  === Beat 1.4: Loops (for & while) ===
  --- Processing AI responses (for loop) ---
  [1] Processed: AI summary ready.
  [skipped empty response]
  [3] Processed: Translation complete.
  [4] Processed: ERROR: timeout

  --- Retrying model call (while loop) ---
  Attempt 1: waiting...
  Attempt 2: Model ready! Stopping retries.
  ```
- **Common mistakes:**
  - Forgetting `attempt += 1` inside a `while` loop, causing an infinite loop.
  - Forgetting indentation (4 spaces) inside the loop block (`IndentationError`).
  - Mixing up `break` (stops the whole loop) and `continue` (skips only the current item).
- **Ask (Student interaction question):**
  - Q: When should you pick a `for` loop vs a `while` loop? — A: Pick `for` when looping over known items or a fixed count (`range()`); pick `while` when repeating until a condition changes (like retries or user typing `quit`).
  - Q: What happens if you forget to update the counter variable inside a `while` loop? — A: The condition stays `True` forever, creating an infinite loop.
- **Done when:** candidates can trace both a `for` loop with `continue` and a `while` loop with a stop condition.

---

### Beat 1.5 – Practical Demonstration & Revision
- **Slides:** Slide 10 (`course/slides/day1-python-i-slides.md`)
- **Learning objective:** Combine setup, variables, data types, `input()` casting, and loops in one complete AI mini-program.
- **Simple technical definition:** A **complete Python script** connects labelled variables, safe user input casting, and loops so data flows cleanly from user input to repeated processing and summary output.
- **Say (Instructor talking points):**
  - Now we put all four pantry skills together into one tiny **AI Prompt Batch Runner**.
  - Notice the flow: configure variables (`model_name`, `tokens_per_run`), ask the user for a task and how many runs (`int(input(...))`), loop that many times with `for`, and track total tokens used.
- **Real-world AI example:** A command-line prompt tester that runs a user's prompt `N` times against a simulated AI model and calculates total token usage across the batch.
- **Python code example:**
  ```python
  model_name = "gpt-4o-mini"
  tokens_per_call = 120
  task = input("Task name: ")
  runs = int(input("How many runs? "))

  total_tokens = 0
  for step in range(1, runs + 1):
      total_tokens += tokens_per_call
      print(f"Run {step}/{runs} on {model_name}: '{task}' complete.")

  print("Total tokens used:", total_tokens)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  printf "Translate text\n2\n" | python3 demos/day1/beat_1_5_revision.py
  ```
  **Point out:** every concept from Day 1 is visible in 15 lines: `str` and `int` variables, `input()` + `int()` casting, `for` loop with `range()`, and running total accumulation.
- **Expected output:**
  ```text
  === Beat 1.5: AI Prompt Batch Runner (Revision) ===
  Run 1/2 on gpt-4o-mini: 'Translate text' -> OK (120 tokens)
  Run 2/2 on gpt-4o-mini: 'Translate text' -> OK (120 tokens)
  Batch finished. Total tokens used: 240
  ```
- **Common mistakes:**
  - Writing `range(runs)` when you want `1` to `runs` (remember `range(2)` produces `0, 1`, while `range(1, runs + 1)` produces `1, 2`).
  - Resetting `total_tokens = 0` inside the loop instead of before the loop.
- **Ask (Student interaction question):**
  - Q: Why do we set `total_tokens = 0` *before* the `for` loop instead of inside it? — A: If you set it inside the loop, it would reset back to `0` on every iteration instead of adding up the total.
- **Done when:** candidates can trace the full batch script from input to final token total.

---

## Exercise (candidates, ~15 min)
Open [exercises/day1_exercise.py](../../exercises/day1_exercise.py) and follow the TODO comments to build a small **AI Token Budget Checker**:
1. Create variables for `model_name` (`str`) and `budget_tokens` (`int`).
2. Ask the user how many prompts they want to test (`int(input(...))`).
3. Use a `for` loop to collect each prompt's token estimate (`int`), skip `0` with `continue`, and stop early with `break` if the running total exceeds `budget_tokens`.
4. Print the final token count and remaining budget.

Run it with: `python3 exercises/day1_exercise.py`

## Done-check (instructor asks the room; agent records the result)
1. Check `python3 --version` and explain what a variable is.
2. Name the 5 basic types (`str`, `int`, `float`, `bool`, `None`) with one AI example each.
3. Explain why `input()` causes the "text trap" and how `int()` / `float()` fixes it.
4. Explain when to use `for` vs `while` (and `break` vs `continue`).
5. Trace a loop that sums token counts across multiple prompts.

## Clean-up
No files are modified by Day 1 demos. Say `end` to save your session summary to `.class/progress.md`.

