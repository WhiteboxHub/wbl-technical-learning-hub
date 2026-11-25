# Instructor Guide

**Python I & Python II (AI Engineering Edition)**, taught with an AI co-pilot (Claude Code) and runnable Python terminal demos.

**In a hurry? See the [Class-day quick start](class-day-quickstart.md).**

---

## 1. How the course works
- **You teach; the agent co-pilots.** It keeps the plan, runs or hands over Python terminal demos, holds the answer key, and tracks progress in `.class/progress.md`. You present the slides and talk to the room.
- **Two independent days:**
  - **Day 1 – Python I (The Labelled Pantry):** Setup, Variables, Data Types, Input & Type Casting, Loops (`for` and `while`).
  - **Day 2 – Python II (The Kitchen's Containers):** Functions (`return` vs `print`), Data Structures, OOP Fundamentals, Big-O Basics & Comprehensions, File Handling.
- **Consistent AI Engineering examples:** Prompts, model names, token counts, temperatures, batch responses, API request/response dictionaries, `AIModel` classes, dataset transforms, and JSON model configs.

| Day | Title | Teach script | Slides | Live demos | Start with |
|---|---|---|---|---|---|
| 1 | Python I | `course/modules/01-python-i.md` | `course/slides/day1-python-i-slides.md` | `demos/day1/` (5 scripts) | `scripts/setup.sh --day1` |
| 2 | Python II | `course/modules/02-python-ii.md` | `course/slides/day2-python-ii-slides.md` | `demos/day2/` (9 scripts) | `scripts/setup.sh --day2` |

## 2. Before your first class (one time)
1. Install **Python 3.10+** and **Claude Code** (desktop app or CLI).
2. Open the `python-course` folder in Claude Code and start a **new session** so `.claude/skills/` loads.
3. Say **"set up the class"** (skill `setup-python-class`). It verifies Python 3, checks all course files, and runs the smoke test (`scripts/smoke.sh`).
4. Open the slide file for the day you are teaching.

## 3. Running a class
Say **"teach day 1"** or **"teach day 2"** (skill `teach-python-class`).

The agent will:
1. Check that Python 3 and that day's demo files are ready.
2. Check `.class/progress.md` and offer to resume if you stopped mid-day earlier.
3. Show objectives, number of beats, estimated time, and slide deck path.
4. Ask **"Is your screen shared?"** Answers stay hidden until you ask for them.
5. Walk one beat at a time: *Slide* → *Talking points & simple definition* → *Real-world AI example & code* → *Live terminal demo* → *Common mistakes* → *Student question* → wait for you.

**Your controls** (plain language works too):

| Say | Effect |
|---|---|
| `next` / `back` | move between beats |
| `repeat` | re-run the demo |
| `skip` | skip and log it |
| `answer` | reveal the answer to the question |
| `more` | another question or example |
| `status` | progress and time used |
| `take over` | you run the demo yourself; the agent waits |
| `jump 1.3` / `jump 2.2` | go to a beat |
| `end` | wrap up |

**At the end** the agent recaps, hands over the practical exercise (`exercises/day1_exercise.py` or `exercises/day2_exercise.py`), runs the done-check, offers a demo cleanup (`scripts/setup.sh --reset`), and saves a post-class note to `.class/progress.md`.

## 4. Day 1 at a glance (~90 min)
| Beat | Topic | Demo script |
|---|---|---|
| 1.1 | Pantry Jars & Variables (Setup + Variables) | `demos/day1/beat_1_1_variables.py` |
| 1.2 | Python Data Types | `demos/day1/beat_1_2_data_types.py` |
| 1.3 | Input & The Text Trap | `demos/day1/beat_1_3_input_casting.py` |
| 1.4 | Loops: Stirring the Pot | `demos/day1/beat_1_4_loops.py` |
| 1.5 | Practical Demonstration & Revision | `demos/day1/beat_1_5_revision.py` |

## 5. Day 2 at a glance (~120–135 min)
| Beat | Topic | Demo script |
|---|---|---|
| 2.1 | Recipe Cards: Return vs Print | `demos/day2/beat_2_1_functions.py` |
| 2.2 | The Four Containers | `demos/day2/beat_2_2_containers.py` |
| 2.3 | OOP: Class and Object | `demos/day2/beat_2_3_oop_class_object.py` |
| 2.4 | OOP: Constructor (`__init__`) | `demos/day2/beat_2_4_oop_constructor.py` |
| 2.5 | OOP: The `self` Keyword | `demos/day2/beat_2_5_oop_self.py` |
| 2.6 | OOP: Attributes and Methods | `demos/day2/beat_2_6_oop_attributes_methods.py` |
| 2.7 | OOP: Inheritance | `demos/day2/beat_2_7_oop_inheritance.py` |
| 2.8 | Comprehensions & Big-O | `demos/day2/beat_2_3_comprehensions_bigo.py` |
| 2.9 | Kitchen Logbook: File I/O | `demos/day2/beat_2_4_file_io.py` |

## 6. Troubleshooting
| Symptom | Fix |
|---|---|
| `python3` not found (exit 10) | Install Python 3.10+ from python.org |
| Python version < 3.10 (exit 11) | Upgrade Python to 3.10 or newer |
| Missing files (exit 12) | Re-check that you are inside `python-course/` |
| Smoke test failed (exit 13) | Check the failed script output, run `scripts/setup.sh --reset`, and retry |
| Skill not found | Open `python-course/` in a **new** Claude Code session |

## 7. After class
Check `.class/progress.md` for skipped beats, confusing topics, and notes. The `.class/` folder is git-ignored and personal to you.

