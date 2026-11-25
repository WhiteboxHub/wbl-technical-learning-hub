# Day 2 — Python II (The Kitchen's Containers)

Teach-skill content file. Format is described in `.claude/skills/teach-python-class/SKILL.md`.
Slides: `course/slides/day2-python-ii-slides.md` (slide numbers below).
Stack requirements: Python 3.10+ installed (`scripts/setup.sh --day2` must be READY). Completely independent from Day 1.
Time: about 120–135 minutes with demos, questions, and exercise.

## Objectives
By the end of Day 2, candidates can write reusable functions that `return` values instead of only printing them, choose among Python's four containers (`list`, `tuple`, `set`, `dict`), build basic classes and objects using OOP fundamentals (Class/Object, `__init__`, `self`, attributes/methods, inheritance), transform datasets with comprehensions while understanding Big-O speed, and read/write text and JSON files safely.

## Stack requirements
- `python3 --version` reports Python 3.10+.
- Demo files present in `demos/day2/`:
  - `beat_2_1_functions.py`
  - `beat_2_2_containers.py`
  - `beat_2_3_oop_class_object.py`
  - `beat_2_4_oop_constructor.py`
  - `beat_2_5_oop_self.py`
  - `beat_2_6_oop_attributes_methods.py`
  - `beat_2_7_oop_inheritance.py`
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

## OOP Fundamentals – Object-Oriented Programming

### Beat 2.3 – Class and Object
- **Slides:** Slides 7–8 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Explain the difference between a class and an object, define a class in Python, and create multiple objects from it.
- **Simple technical definition:** A **class** is a blueprint (template) that defines what data and actions something should have. An **object** is a real item built from that blueprint—each object is its own separate instance in memory.
- **Say (Instructor talking points):**
  - Yesterday and earlier today we stored data in loose variables or dictionaries. As AI apps grow, keeping a model's name, settings, and actions bundled together makes code much cleaner.
  - A **class** is like a cookie cutter or kitchen recipe template (`class AIModel:`); an **object** (`fast_model = AIModel()`) is an actual cookie or dish made from it.
  - You write the `class` once and can create as many objects from it as you want.
- **Why this concept is important:** Without classes, you have to pass separate dictionaries and helper functions around everywhere; classes group related data and behavior in one clean unit.
- **Real-world example:** A car factory blueprint (`Car` class) vs actual cars parked outside (`car_1`, `car_2`). Both follow the same design, but they are separate physical cars.
- **AI Engineering example:** An `AIModel` class acts as the blueprint for a model client, and `fast_model` and `smart_model` are two separate objects created from that blueprint.
- **Python code example:**
  ```python
  class AIModel:
      provider = "local-demo"

  fast_model = AIModel()
  smart_model = AIModel()
  print(fast_model is smart_model)  # False: two separate objects!
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_3_oop_class_object.py
  ```
  **Point out:** `fast_model` and `smart_model` both have type `AIModel`, yet `fast_model is smart_model` prints `False` because each `AIModel()` call creates a brand-new object.
- **Expected output:**
  ```text
  === Beat 2.3: Class and Object ===
  Class blueprint : <class '__main__.AIModel'>
  Object 1        : <class '__main__.AIModel'> | provider = local-demo
  Object 2        : <class '__main__.AIModel'> | provider = local-demo
  Same object?    : False
  ```
- **Common mistakes:**
  - Forgetting the parentheses `()` when creating an object (`m = AIModel` refers to the class itself instead of creating an object).
  - Using lowercase for class names instead of `PascalCase` (convention is `AIModel`, not `ai_model`).
- **Ask (Student interaction question):**
  - Q: If you write `model_a = AIModel()` and `model_b = AIModel()`, how many classes exist and how many objects exist? — A: One class (`AIModel`) and two objects (`model_a` and `model_b`).
- **Done when:** candidates can define an empty/simple class and create two separate objects from it.

---

### Beat 2.4 – Constructor (`__init__`)
- **Slides:** Slide 9 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Use `__init__` to automatically give each new object its own starting values when it is created.
- **Simple technical definition:** **`__init__`** (short for initialize, with two underscores on each side) is a special **constructor** method inside a class. Python runs it **automatically** every time you create a new object so the object starts with the exact values you pass in.
- **Say (Instructor talking points):**
  - In Beat 2.3, both `fast_model` and `smart_model` looked identical when created. Usually, each object needs its own starting settings right away.
  - Adding `def __init__(self, name, temperature):` lets you write `AIModel("gpt-4o-mini", 0.2)` and set those values automatically upon creation.
  - Notice you never call `__init__` directly by name—calling `AIModel(...)` triggers `__init__` behind the scenes.
- **Why this concept is important:** Constructors prevent half-built objects with missing settings by forcing required setup values when the object is created.
- **Real-world example:** Filling out a coffee order ticket when you place an order: size (`"large"`) and roast (`"dark"`) are recorded immediately so the cup starts with the right settings.
- **AI Engineering example:** Initializing one `AIModel("gpt-4o-mini", 0.2)` for deterministic summaries and another `AIModel("gemini-2.5-flash", 0.9)` for creative brainstorming.
- **Python code example:**
  ```python
  class AIModel:
      def __init__(self, name, temperature):
          self.name = name
          self.temperature = temperature

  fast_model = AIModel("gpt-4o-mini", 0.2)
  creative_model = AIModel("gemini-2.5-flash", 0.9)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_4_oop_constructor.py
  ```
  **Point out:** the `[__init__ called]` message prints automatically each time `AIModel(...)` runs, and both objects end up with different `name` and `temperature` values.
- **Expected output:**
  ```text
  === Beat 2.4: Constructor (__init__) ===
  [__init__ called] Setting up gpt-4o-mini...
  [__init__ called] Setting up gemini-2.5-flash...
  Model 1: name=gpt-4o-mini, temp=0.2
  Model 2: name=gemini-2.5-flash, temp=0.9
  ```
- **Common mistakes:**
  - Typing only one underscore (`_init_`) instead of two (`__init__`)—Python will silently ignore it and not run it on creation.
  - Trying to `return` a value from `__init__` (`TypeError: __init__() should return None`).
  - Passing the wrong number of arguments when creating the object (`TypeError: missing required positional argument`).
- **Ask (Student interaction question):**
  - Q: When does Python run `__init__`, and do you call `obj.__init__()` manually? — A: Python runs `__init__` automatically at the moment you create an object like `AIModel("gpt-4o-mini", 0.2)`; you do not call it manually.
- **Done when:** candidates can write an `__init__` method that accepts two arguments and sets them on the object.

---

### Beat 2.5 – The `self` Keyword
- **Slides:** Slide 10 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Explain what `self` represents inside a class and why methods must list `self` as their first parameter.
- **Simple technical definition:** **`self`** is a variable representing **"this specific object right here"**—whichever object is currently running the method. Python automatically passes the object as the first argument (`self`) whenever you call `obj.method()`.
- **Say (Instructor talking points):**
  - If you have two objects (`summary_model` and `story_model`) sharing the same class code, how does a method know which object's temperature to print?
  - That is what **`self`** solves: when you call `summary_model.show_config()`, Python quietly translates it into `AIModel.show_config(summary_model)`, so `self` is `summary_model`!
  - Rule of thumb: **write `self` as the first parameter when defining a method, and do NOT pass `self` when calling the method.**
- **Why this concept is important:** Without `self`, an object's methods could not tell one object's data apart from another's, and setting `name = name` inside `__init__` would vanish as a local variable instead of saving onto the object.
- **Real-world example:** Two bank accounts (`alice_acct`, `bob_acct`) built from one `BankAccount` class. Calling `alice_acct.show_balance()` needs `self` so it reads Alice's balance, not Bob's.
- **AI Engineering example:** Keeping `summary_model` (`temp=0.1`) and `story_model` (`temp=0.8`) completely isolated so calling `show_config()` on each reads its own configuration via `self.name` and `self.temperature`.
- **Python code example:**
  ```python
  class AIModel:
      def __init__(self, name, temperature):
          self.name = name
          self.temperature = temperature

      def show_config(self):
          print(f"Config -> model={self.name}, temperature={self.temperature}")

  summary_model = AIModel("gpt-4o-mini", 0.1)
  summary_model.show_config()
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_5_oop_self.py
  ```
  **Point out:** calling `summary_model.show_config()` prints `0.1` while `story_model.show_config()` prints `0.8` using the exact same `show_config(self)` code.
- **Expected output:**
  ```text
  === Beat 2.5: The self Keyword ===
  Config -> model=gpt-4o-mini, temperature=0.1
  Config -> model=claude-haiku, temperature=0.8
  ```
- **Common mistakes:**
  - Forgetting `self` in the method definition (`def show_config():` → `TypeError: takes 0 positional arguments but 1 was given`).
  - Forgetting `self.` when saving or reading an attribute inside the class (`name = name` instead of `self.name = name`).
- **Ask (Student interaction question):**
  - Q: In `def show_config(self):`, why do we call `summary_model.show_config()` with empty parentheses `()` even though `self` is in the definition? — A: Because Python automatically passes `summary_model` in as `self` for you.
- **Done when:** candidates can explain what `self` points to when two different objects call the same method.

---

### Beat 2.6 – Attributes and Methods
- **Slides:** Slide 11 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Distinguish between instance attributes (data) and instance methods (actions) on an object.
- **Simple technical definition:** **Instance attributes** are variables stored inside an object (`self.name`, `self.call_count`) that hold its data. **Instance methods** are functions defined inside a class (`def generate_response(self, prompt):`) that define what the object can do and can read or update its attributes.
- **Say (Instructor talking points):**
  - Think in simple grammar: **attributes are nouns** (what an object *has*—name, temperature, call count), and **methods are verbs** (what an object *does*—generate a response).
  - Remember: attributes are accessed without parentheses (`assistant.call_count`), while methods are called with parentheses (`assistant.generate_response("...")`).
  - Methods can update the object's own attributes—for example, counting how many prompts this model object has answered.
- **Why this concept is important:** Combining attributes and methods lets one object track its own state (like usage count) while providing clean actions (`generate_response()`) to the rest of your AI application.
- **Real-world example:** A coffee machine object has **attributes** (`water_level`, `beans_grams`) and **methods** (`brew_espresso()`), where brewing lowers the water level.
- **AI Engineering example:** An `AIModel` object stores `name`, `temperature`, and `call_count` as instance attributes, and defines `generate_response(self, prompt)` as an instance method that returns a simulated reply and increments `self.call_count`.
- **Python code example:**
  ```python
  class AIModel:
      def __init__(self, name, temperature):
          self.name = name
          self.temperature = temperature
          self.call_count = 0

      def generate_response(self, prompt):
          self.call_count += 1
          return f"[{self.name} | temp={self.temperature}] Simulated answer to: '{prompt}'"

  assistant = AIModel("gpt-4o-mini", 0.3)
  print(assistant.generate_response("Explain Python classes"))
  print("Calls made:", assistant.call_count)
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_6_oop_attributes_methods.py
  ```
  **Point out:** each call to `assistant.generate_response(...)` returns a formatted string AND increases `assistant.call_count` from `0` to `2`.
- **Expected output:**
  ```text
  === Beat 2.6: Attributes and Methods ===
  Reply 1    : [gpt-4o-mini | temp=0.3] Simulated answer to: 'Explain Python classes'
  Reply 2    : [gpt-4o-mini | temp=0.3] Simulated answer to: 'Summarize Big-O'
  Calls made : 2
  ```
- **Common mistakes:**
  - Calling an attribute like a method (`assistant.call_count()` → `TypeError: 'int' object is not callable`).
  - Accessing a method without `()` (`assistant.generate_response` prints `<bound method ...>` instead of running it).
- **Ask (Student interaction question):**
  - Q: In `assistant.call_count` vs `assistant.generate_response("Hi")`, which one is an attribute and which one is a method, and how can you tell? — A: `call_count` is an attribute (data, no parentheses), and `generate_response(...)` is a method (an action, called with parentheses).
- **Done when:** candidates can add a new attribute and a new method to `AIModel` and use both.

---

### Beat 2.7 – Inheritance
- **Slides:** Slides 12–13 (`course/slides/day2-python-ii-slides.md`)
- **Learning objective:** Create a child class from a parent class using `class Child(Parent):` to reuse existing attributes and methods.
- **Simple technical definition:** **Inheritance** allows a **child class** (subclass) to reuse all attributes and methods from an existing **parent class** (base class), and then add new specialized attributes or methods of its own without copying code.
- **Say (Instructor talking points):**
  - Suppose `AIModel` already handles `name`, `temperature`, and `generate_response()`. Now we also want a `ChatModel` that keeps a `system_prompt` and has a `chat()` helper.
  - Instead of copy-pasting `AIModel`'s code, we write `class ChatModel(AIModel):`—putting the parent class in parentheses!
  - `ChatModel` automatically gets `__init__`, `self.name`, `self.temperature`, and `generate_response()` for free, and only writes the new chat-specific parts.
- **Why this concept is important:** Inheritance avoids repeating code across similar classes and keeps shared AI configuration logic in one place.
- **Real-world example:** A general `Vehicle` parent class (has `speed` and `start()`) and a specialized `ElectricCar(Vehicle)` child class that reuses `speed` and `start()` while adding `charge_battery()`.
- **AI Engineering example:** `ChatModel(AIModel)` inherits `name`, `temperature`, and `generate_response()` from `AIModel`, and adds `set_system_prompt()` and `chat(user_message)` to build chat-style prompts.
- **Python code example:**
  ```python
  class AIModel:
      def __init__(self, name, temperature):
          self.name = name
          self.temperature = temperature

      def generate_response(self, prompt):
          return f"[{self.name} | temp={self.temperature}] {prompt}"

  class ChatModel(AIModel):
      def set_system_prompt(self, system_prompt):
          self.system_prompt = system_prompt

      def chat(self, user_message):
          return self.generate_response(f"System({self.system_prompt}) -> User({user_message})")
  ```
- **Live terminal demonstration (run: agent):**
  ```bash
  python3 demos/day2/beat_2_7_oop_inheritance.py
  ```
  **Point out:** `ChatModel` never defined `__init__` or `generate_response`, yet `bot.name` and `bot.generate_response(...)` both work because `ChatModel` inherited them from `AIModel`.
- **Expected output:**
  ```text
  === Beat 2.7: Inheritance ===
  Inherited name : gpt-4o-mini
  Inherited call : [gpt-4o-mini | temp=0.2] Hello AI
  Child chat call: [gpt-4o-mini | temp=0.2] System(Be brief and beginner-friendly) -> User(What is inheritance?)
  ```
- **Common mistakes:**
  - Forgetting `(AIModel)` after the child class name (`class ChatModel:` creates an unrelated class that does not inherit `AIModel`).
  - Trying to call a child-only method (`chat()`) on a plain parent `AIModel` object (inheritance flows from parent → child, not child → parent).
- **Ask (Student interaction question):**
  - Q: Why did `bot = ChatModel("gpt-4o-mini", 0.2)` work even though `ChatModel` did not define its own `__init__` method? — A: Because `ChatModel` inherited `__init__` from its parent class `AIModel`.
- **Done when:** candidates can identify the parent and child class in `class ChatModel(AIModel):` and explain what gets reused.

---

### Beat 2.8 – Comprehensions & Big-O
- **Slides:** Slides 14–16 (`course/slides/day2-python-ii-slides.md`)
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

### Beat 2.9 – Kitchen Logbook: File I/O
- **Slides:** Slides 17–19 (`course/slides/day2-python-ii-slides.md`)
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
2. Create an `AIModel(name, temperature)` class with `__init__`, `self`, and a `generate_response(prompt)` method.
3. Read `demos/day2/data/model_config.json` using `with open(...)` and `json.load()`, instantiate `AIModel` from the loaded config, and print the returned summary plus a simulated response.

Run it with: `python3 exercises/day2_exercise.py`

## Done-check (instructor asks the room; agent records the result)
1. Explain the difference between `print()` and `return`.
2. Choose between `list`, `tuple`, `set`, and `dict` for four AI use cases.
3. Explain class vs object, `__init__`, `self`, attributes vs methods, and inheritance using `AIModel`.
4. Write a simple list comprehension and explain `O(1)` vs `O(n)` vs `O(n^2)`.
5. Read a JSON file and append to a log file using `with open(...)`.

## Clean-up
Run `scripts/setup.sh --reset` to remove `run_log.txt` and `updated_config.json` generated during Beat 2.9. Say `end` to save your session summary to `.class/progress.md`.

