# Day 2 — Python II (The Kitchen's Containers)

Teach-skill content file. Format is described in `.claude/skills/teach-python-class/SKILL.md`.
Slides: `course/slides/day2-python-ii-slides.md` (slide numbers below).
Stack requirements: Python 3.10+ installed (`scripts/setup.sh --day2` must be READY). Completely independent from Day 1.
Time: about 90 minutes with demos, questions, and exercise.

## Objectives
By the end of Day 2, candidates can write reusable functions that `return` values instead of only printing them, choose among Python's four containers (`list`, `tuple`, `set`, `dict`), transform datasets with comprehensions while understanding Big-O speed, and read/write text and JSON files safely.

## Stack requirements
- `python3 --version` reports Python 3.10+.
- Demo files present in `demos/day2/`:
  - `beat_2_1_functions.py`
  - `beat_2_2_containers.py`
  - `beat_2_3_comprehensions_bigo.py`
  - `beat_2_4_file_io.py`
  - `data/model_config.json`
  - `data/prompt_docs.txt`
- Exercise file: `exercises/day2_exercise.py`.

---

### Beat 2.1 – Recipe Cards: Return vs Print
- **Slides:** Slides 1–3 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Define reusable functions with parameters and explain why `return` is different from `print()`.
- **Simple technical definition:** A **function** (`def`) is a reusable named block of code that takes inputs (parameters) and hands back an output. **`print()`** only displays text on the screen for humans; **`return`** sends an actual value back to your Python code so you can store or reuse it.
- **Say (Instructor talking points):**
  - Think of a function like a **recipe card**: instead of writing the steps to calculate token cost every single time, you write the recipe once and call it whenever you need it.
  - The biggest beginner bug with functions is using `print()` when you meant `return`. If a function has no `return`, Python silently hands back `None`.
  - Use `return` inside helper functions so the rest of your program can keep working with the result.
- **Real-world AI example:** Writing an `estimate_cost(tokens, price_per_1k)` helper function in an AI pipeline. If it `print`s the cost instead of `return`ing it, you cannot add multiple API calls together!
- **Python code example:**
  ```python
  def print_only_cost(tokens):
      print((tokens / 1000) * 0.002)

  def calculate_cost(tokens, price_per_1k=0.002):
      return (tokens / 1000) * price_per_1k

  result_bad = print_only_cost(1500)     # prints 0.003, stores None!
  result_good = calculate_cost(1500)     # stores 0.003 so we can reuse it
  print("Bad stored value :", result_bad)
  print("Total 2 calls ($):", result_good * 2)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_1_functions.py
  ```
  **Point out:** `result_bad` is `None` (trying to multiply it crashes), while `result_good` holds `0.003` and can be added, doubled, or formatted.
- **Expected output:**
  ```text
  === Beat 2.1: Recipe Cards (Return vs Print) ===
  0.003
  print_only_cost returned : None
  calculate_cost returned  : 0.003
  Two API calls total ($)  : 0.006
  ```
- **Common mistakes:**
  - Writing `print(...)` inside a calculation function and getting `TypeError: unsupported operand type(s) for +: 'NoneType' and 'float'` later.
  - Putting code *after* `return` inside a function (anything after `return` never runs).
  - Defining a function with `def ...` and forgetting to actually **call** it with `()`.
- **Ask (Student interaction question):**
  - Q: What value does `x = greet()` store if `greet()` only calls `print("Hi")` and has no `return` statement? — A: `None`.
  - Q: Why should AI processing functions usually `return` data instead of `print`ing it? — A: So the caller can pass that result into another function, save it to a file, or combine it with other results.
- **Done when:** candidates can explain why `print_only_cost()` returns `None` and rewrite it with `return`.

---

### Beat 2.2 – The Four Containers
- **Slides:** Slides 4–6 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Choose the right Python container (`list`, `tuple`, `set`, `dict`) for a given AI Engineering task.
- **Simple technical definition:** Python has four built-in containers for grouping values: **`list`** (ordered, changeable `[...]`), **`tuple`** (ordered, fixed `(...)`), **`set`** (unique items, unordered `{...}`), and **`dict`** (key-to-value lookup pairs `{key: value}`).
- **Say (Instructor talking points):**
  - Every kitchen needs different containers: a **list** is a tray of responses in order; a **tuple** is a sealed label that cannot be edited by mistake; a **set** is a jar of unique tags with no duplicates; a **dict** is a labelled drawer where you look things up by name (`key`).
  - In AI Engineering, **lists** hold multiple model responses or messages, **tuples** hold fixed `(width, height)` or `(model, version)` pairs, **sets** deduplicate stop words or user IDs, and **dicts** represent JSON API requests and responses.
- **Real-world AI example:** Storing three candidate responses from an LLM (`list`), locking a model's `(provider, model_id)` pair (`tuple`), collecting unique topic tags (`set`), and building an API request payload `{"model": "gpt-4o-mini", "temperature": 0.2}` (`dict`).
- **Python code example:**
  ```python
  responses = ["Summary A", "Summary B", "Summary A"]     # list (ordered, allows duplicates)
  model_spec = ("openai", "gpt-4o-mini")                  # tuple (fixed, cannot modify)
  unique_tags = {"ai", "python", "ai"}                    # set (duplicates removed -> {"ai", "python"})
  api_request = {"model": model_spec[1], "temperature": 0.2, "max_tokens": 150}  # dict

  print("First response:", responses[0])
  print("Unique tags   :", unique_tags)
  print("Request temp  :", api_request["temperature"])
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_2_containers.py
  ```
  **Point out:** `"ai"` appears only once in the `set`; accessing `api_request["model"]` looks up the value by key name instead of index number.
- **Expected output:**
  ```text
  === Beat 2.2: The Four Containers ===
  list  (responses)  : ['Summary A', 'Summary B', 'Summary A']
  tuple (model_spec) : ('openai', 'gpt-4o-mini')
  set   (unique_tags): {'ai', 'python'} (count = 2)
  dict  (api_request): {'model': 'gpt-4o-mini', 'temperature': 0.2, 'max_tokens': 150}
  ```
- **Common mistakes:**
  - Writing `{}` expecting an empty `set` (`{}` creates an empty `dict`; use `set()` for an empty set).
  - Accessing a missing dict key with `d["missing"]` (`KeyError`) instead of `d.get("missing")`.
  - Trying to change an item inside a `tuple` (`TypeError: 'tuple' object does not support item assignment`).
- **Ask (Student interaction question):**
  - Q: Which container should you pick to store an AI API request with `"model"`, `"prompt"`, and `"temperature"`? — A: A `dict` (dictionary), because every setting has a clear key name.
  - Q: Which container automatically removes duplicate words from a list of tokens? — A: A `set`.
- **Done when:** candidates can pick the right container (`list`, `tuple`, `set`, `dict`) for four scenarios.

---

### Beat 2.3 – Comprehensions & Big-O
- **Slides:** Slides 7–9 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Transform datasets cleanly with comprehensions and compare `O(1)`, `O(n)`, and `O(n^2)` search speed.
- **Simple technical definition:** A **comprehension** is a short one-line way to build a new `list` or `dict` from an existing collection. **Big-O notation** measures how the number of steps grows as your dataset gets bigger: **`O(1)`** takes 1 instant step regardless of size, **`O(n)`** grows linearly with `n` items, and **`O(n^2)`** compares every item with every other item.
- **Say (Instructor talking points):**
  - In AI data prep, you constantly clean prompts or measure response lengths. A list comprehension `[len(r) for r in responses]` replaces a 4-line `for` + `.append()` loop.
  - **Big-O in one kitchen rule:** looking up a key in a `dict` or `set` is like checking a labelled drawer—**`O(1)`** instant, whether you have 10 items or 1,000,000! Checking `x in my_list` scans item by item—**`O(n)`**. Nested loops (`for a in items: for b in items:`) grow as **`O(n^2)`** and become very slow on large datasets.
- **Real-world AI example:** Cleaning a dataset of raw user prompts with a list comprehension, building a `{prompt: length}` dictionary comprehension, and measuring how much faster `set` / `dict` membership lookup (`O(1)`) is compared to `list` scanning (`O(n)`) across 50,000 banned/stop words.
- **Python code example:**
  ```python
  raw_prompts = ["  Summarize AI ", "Explain BIG-O  ", ""]
  clean_prompts = [p.strip().lower() for p in raw_prompts if p.strip()]
  prompt_lengths = {p: len(p) for p in clean_prompts}

  # Big-O lookup comparison: list O(n) vs set O(1)
  id_list = list(range(50_000))
  id_set = set(id_list)
  print("49999 in set (O(1)):", 49999 in id_set)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_3_comprehensions_bigo.py
  ```
  **Point out:** the comprehension strips whitespace and drops the empty string in one readable line; the timing benchmark shows `set` (`O(1)`) is orders of magnitude faster than `list` (`O(n)`) for repeated lookups.
- **Expected output:**
  ```text
  === Beat 2.3: Comprehensions & Big-O ===
  Clean prompts  : ['summarize ai', 'explain big-o']
  Length map     : {'summarize ai': 12, 'explain big-o': 13}
  Big-O check (1,000 lookups in 50,000 items):
    list O(n) scan : ~... ms
    set  O(1) hash : ~... ms (much faster!)
  ```
- **Common mistakes:**
  - Writing overly complex nested comprehensions that become hard to read (keep comprehensions simple; use a normal `for` loop if logic gets complex).
  - Doing `if word in huge_list:` inside a loop over thousands of documents (`O(n^2)` total!) instead of converting `huge_list` to a `set` once.
- **Ask (Student interaction question):**
  - Q: Why is `token in stop_words_set` faster than `token in stop_words_list` on 100,000 words? — A: A `set` uses a hash lookup in `O(1)` time, while a `list` scans item by item in `O(n)` time.
  - Q: Write a list comprehension that turns `["hi", "ai"]` into `["HI", "AI"]`. — A: `[w.upper() for w in ["hi", "ai"]]`.
- **Done when:** candidates can write a basic comprehension and explain `O(1)` vs `O(n)` vs `O(n^2)`.

---

### Beat 2.4 – Kitchen Logbook: File I/O
- **Slides:** Slides 10–12 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Read text files, load/save JSON configuration files, and append logs safely using `with open(...)`.
- **Simple technical definition:** **File I/O (Input/Output)** lets Python read data from files on disk and save results back to files. Using **`with open(...) as f:`** automatically closes the file when the block finishes, even if an error happens. Python's built-in **`json`** module converts between JSON files and Python `dict`/`list` objects.
- **Say (Instructor talking points):**
  - Variables disappear when a Python script finishes—files are the **kitchen logbook** that survives after the program stops.
  - Always use `with open(path, mode, encoding="utf-8") as f:` instead of calling `open()` without `with`.
  - Modes to know: `"r"` = read, `"w"` = write (overwrites file!), `"a"` = append (adds to the end, great for logs).
  - For AI settings and datasets, **`json.load(f)`** reads a `.json` file straight into a Python `dict`, and **`json.dump(data, f, indent=2)`** writes a `dict` back to disk.
- **Real-world AI example:** Loading `demos/day2/data/model_config.json` for model settings, reading `demos/day2/data/prompt_docs.txt` as source context lines, and appending an entry to `demos/day2/data/run_log.txt`.
- **Python code example:**
  ```python
  import json

  with open("demos/day2/data/model_config.json", "r", encoding="utf-8") as f:
      config = json.load(f)

  with open("demos/day2/data/prompt_docs.txt", "r", encoding="utf-8") as f:
      lines = [line.strip() for line in f if line.strip()]

  with open("demos/day2/data/run_log.txt", "a", encoding="utf-8") as f:
      f.write(f"Loaded {len(lines)} docs for model={config['model']}\n")
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_4_file_io.py
  ```
  **Point out:** `json.load()` gives us a real Python `dict` (`config["model"]`), `prompt_docs.txt` lines are read cleanly, and `run_log.txt` persists on disk after the script exits.
- **Expected output:**
  ```text
  === Beat 2.4: Kitchen Logbook (File I/O) ===
  Loaded model config : gpt-4o-mini (temp=0.2, max_tokens=300)
  Loaded document lines: 3
  Appended run entry to demos/day2/data/run_log.txt
  Saved updated config to demos/day2/data/updated_config.json
  ```
- **Common mistakes:**
  - Opening an existing log file with `"w"` instead of `"a"` and accidentally erasing all previous logs.
  - Using `json.loads()` (for strings) instead of `json.load()` (for file objects), or forgetting `encoding="utf-8"`.
  - Running the script from the wrong working directory so relative paths like `demos/day2/data/...` raise `FileNotFoundError`.
- **Ask (Student interaction question):**
  - Q: Why is `with open(...) as f:` safer than `f = open(...)`? — A: `with` guarantees Python closes the file automatically when the block ends, even if an error occurs.
  - Q: Which file mode should you use to add a new line to an existing log file without deleting old lines? — A: `"a"` (append), not `"w"` (write/overwrite).
- **Done when:** candidates can read a `.txt` and `.json` file with `with open(...)` and explain `"r"` vs `"w"` vs `"a"`.

---

## Exercise (candidates, ~20 min)
Open [exercises/day2_exercise.py](../../exercises/day2_exercise.py) and complete the TODOs to build a **Model Config & Prompt Analyzer**:
1. Write a function `analyze_prompts(prompts)` that **returns** a `dict` containing total count, unique prompt count (using a `set`), and a list of cleaned prompts (using a list comprehension).
2. Read `demos/day2/data/model_config.json` using `with open(...)` and `json.load()`.
3. Print the returned summary alongside the loaded model name.

Run it with: `python3 exercises/day2_exercise.py`

## Done-check (instructor asks the room; agent records the result)
1. Explain the difference between `print()` and `return`.
2. Choose between `list`, `tuple`, `set`, and `dict` for four AI use cases.
3. Write a simple list comprehension and explain `O(1)` vs `O(n)` vs `O(n^2)`.
4. Read a JSON file and append to a log file using `with open(...)`.

## Clean-up
Run `scripts/setup.sh --reset` to remove `run_log.txt` and `updated_config.json` generated during Beat 2.4. Say `end` to save your session summary to `.class/progress.md`.

