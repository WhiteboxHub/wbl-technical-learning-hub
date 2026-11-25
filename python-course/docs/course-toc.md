# Python for AI Engineering — Table of Contents

Two-day beginner course. Theme: **AI Engineering Kitchen** (prompts, models, tokens, datasets, configs, and logs).
Environment: Local Python 3.10+ (zero external package dependencies required).

| Day | Module | Title | Metaphor | Beats |
|---|---|---|---|---|
| **Day 1** | 1 | Python I | The Labelled Pantry | 5 beats (1.1 – 1.5) |
| **Day 2** | 2 | Python II | The Kitchen's Containers | 4 beats (2.1 – 2.4) |

---

## Day 1 – Python I (The Labelled Pantry)

Topics:
1. Python Introduction & Setup
2. Variables
3. Data Types
4. Input & Type Casting
5. Loops (`for` and `while`)

Beats:
- **Beat 1.1 – Pantry Jars & Variables:** Python setup check, naming and assigning variables (prompt, model name, temperature), reassigning values.
- **Beat 1.2 – Python Data Types:** `str`, `int`, `float`, `bool`, and `None` using token counts, temperature, model names, and streaming flags.
- **Beat 1.3 – Input & The Text Trap:** Reading user prompts and numeric inputs with `input()`, why `input()` always returns `str`, and fixing it with `int()` / `float()`.
- **Beat 1.4 – Loops: Stirring the Pot:** `for` loops to process multiple AI responses, `while` loops for retry/token-budget control, `break` and `continue`.
- **Beat 1.5 – Practical Demonstration & Revision:** End-to-end mini prompt-batch processor combining setup, variables, types, casting, and loops.

---

## Day 2 – Python II (The Kitchen's Containers)

Topics:
1. Functions (`return` vs `print`)
2. Data Structures (`list`, `tuple`, `set`, `dict`)
3. Big-O Basics (and Comprehensions)
4. File Handling

Beats:
- **Beat 2.1 – Recipe Cards: Return vs Print:** Writing reusable AI helper functions, why `print()` shows text while `return` passes values back (`None` trap).
- **Beat 2.2 – The Four Containers:** Comparing `list` (ordered responses), `tuple` (fixed model coordinates/settings), `set` (unique stop words/tags), and `dict` (API request/response payloads).
- **Beat 2.3 – Comprehensions & Big-O:** List/dict comprehensions for transforming datasets, plus `O(1)` dict/set lookup vs `O(n)` list scan vs `O(n^2)` nested loops.
- **Beat 2.4 – Kitchen Logbook: File I/O:** Using `with open(...)` safely to read text documents, load/save JSON model configurations (`json`), and append run logs.

---

## Every Day Ships With
Teach script (`course/modules/`) · Slide deck (`course/slides/`) · Runnable terminal demos (`demos/`) · Practical exercise (`exercises/`) · Automated smoke & unit checks (`scripts/` & `exercises/tests/`).

