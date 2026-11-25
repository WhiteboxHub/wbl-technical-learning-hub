# Student Guide

Welcome to **Python I & Python II (AI Engineering Edition)**. You will learn core Python by running real terminal programs themed around an **AI Engineering Kitchen** (prompts, models, tokens, datasets, and config files).

## 1. What you will learn

### Day 1 – Python I (The Labelled Pantry)
| Beat | Topic | You will be able to… |
|---|---|---|
| 1.1 | Python Setup & Variables | Check Python, create variables for prompts/models, and reassign values |
| 1.2 | Python Data Types | Use `str`, `int`, `float`, `bool`, and `None` accurately |
| 1.3 | Input & Type Casting | Read user input and convert strings using `int()` and `float()` |
| 1.4 | Loops (`for` & `while`) | Process batches of AI responses and control retries with `break`/`continue` |
| 1.5 | Practical Revision | Combine variables, types, casting, and loops in one working script |

### Day 2 – Python II (The Kitchen's Containers)
| Beat | Topic | You will be able to… |
|---|---|---|
| 2.1 | Functions (`return` vs `print`) | Write reusable AI helper functions and avoid the `None` return trap |
| 2.2 | The Four Containers | Choose between `list`, `tuple`, `set`, and `dict` |
| 2.3–2.7 | OOP Fundamentals | Create classes and objects, use `__init__` & `self`, attributes/methods, and inheritance |
| 2.8 | Comprehensions & Big-O | Transform datasets in one line and compare `O(1)` vs `O(n)` vs `O(n^2)` |
| 2.9 | File Handling | Read text/JSON configs and write run logs safely using `with open(...)` |

---

## 2. Get your laptop ready (before class)
You need:
- **Python 3.10 or newer**: check with `python3 --version` (install from https://www.python.org/downloads/ if missing)
- **A terminal** (macOS Terminal, Linux shell, or Windows PowerShell / WSL2 / Git Bash)
- **Claude Code** (optional, to run the study coach and setup helper)

Then:
1. Open the `python-course` folder in Claude Code (start a **new session** after opening it).
2. Say **"set up my environment"** (or run `bash scripts/setup.sh` in your terminal).
3. When it prints **READY**, run your first Python demo:
   ```bash
   python3 demos/day1/beat_1_1_variables.py
   ```

---

## 3. Cheat Sheets

### Day 1 Cheat Sheet
```python
# Variables (Labelled Pantry Jars)
model_name = "gpt-4o-mini"       # str
max_tokens = 250                 # int
temperature = 0.7                # float
stream_mode = True               # bool
last_error = None                # NoneType

# Input & Type Casting (input() ALWAYS returns str)
user_prompt = input("Prompt: ")
limit = int(input("Max tokens: "))
temp = float(input("Temperature: "))

# Loops
for response in ["OK", "Retry", "Done"]:
    print(response)

retries = 0
while retries < 3:
    retries += 1
```

### Day 2 Cheat Sheet
```python
# Functions: return gives data back; print only displays on screen
def estimate_cost(tokens, rate=0.002):
    return (tokens / 1000) * rate

# Four Containers
responses = ["Yes", "No", "Yes"]       # list: ordered, changeable
model_dims = (1536, 128000)            # tuple: ordered, fixed (immutable)
stop_words = {"the", "a", "an"}        # set: unique, unordered, fast O(1) lookup
payload = {"model": "mini", "temp": 0} # dict: key -> value, fast O(1) lookup

# OOP Fundamentals (Class, __init__, self, Attributes/Methods, Inheritance)
class AIModel:
    def __init__(self, name, temperature):
        self.name = name
        self.temperature = temperature

    def generate_response(self, prompt):
        return f"[{self.name}] {prompt}"

class ChatModel(AIModel):
    def chat(self, message):
        return self.generate_response(f"Chat: {message}")

# List & Dict Comprehensions
lengths = [len(r) for r in responses]
upper_map = {r: r.upper() for r in responses}

# File Handling
import json
with open("demos/day2/data/model_config.json", "r", encoding="utf-8") as f:
    config = json.load(f)
```

---

## 4. Exercises
- **Day 1 Exercise:** Open and complete [exercises/day1_exercise.py](../exercises/day1_exercise.py)
- **Day 2 Exercise:** Open and complete [exercises/day2_exercise.py](../exercises/day2_exercise.py)

Run your exercise script in the terminal:
```bash
python3 exercises/day1_exercise.py
python3 exercises/day2_exercise.py
```

---

## 5. Practice after class
In Claude Code, inside the `python-course` folder, say:
- **"quiz me on day 1"** or **"quiz me on day 2"**: one question at a time with instant feedback
- **"help with the day 1 exercise"** (or **day 2**): hints first, checks your Python code
- **"explain Big-O"** (or any syllabus topic): plain-English explanation with an AI example
- **"check my progress on day 1"**: walks the self-check and saves your progress

