# Python for AI Engineering — Course Repo

Running theme: **AI Engineering Kitchen** — learn core Python using real AI workflows (prompts, model names, token counts, temperatures, datasets, JSON configs, and log files).

## Choose Your Day

This course is organized into **two independent days**:

| Day | Title | Topics | Module File |
|---|---|---|---|
| **Day 1** | **Python I (The Labelled Pantry)** | Python Setup, Variables, Data Types, Input & Type Casting, Loops (`for` and `while`) | [01-python-i.md](course/modules/01-python-i.md) |
| **Day 2** | **Python II (The Kitchen's Containers)** | Functions (`return` vs `print`), Data Structures (`list`, `tuple`, `set`, `dict`), Comprehensions & Big-O Basics, File Handling | [02-python-ii.md](course/modules/02-python-ii.md) |

## Guides
- [Class-day quick start](docs/class-day-quickstart.md) — 5-minute instructor checklist
- [Instructor Guide](docs/instructor-guide.md) — setup, running Day 1 or Day 2 with the AI co-pilot, troubleshooting
- [Student Guide](docs/student-guide.md) — laptop setup, Day 1 & Day 2 cheat sheets, and exercises
- [Instructor Steps](instructor-steps.md) — day-of commands for starting, teaching, and wrapping up
- [Course Table of Contents](docs/course-toc.md) — full syllabus and beat list

## Quick Start
Requires **Python 3.10+** installed.

```bash
scripts/setup.sh
```

To verify a single day independently:
```bash
scripts/setup.sh --day1
scripts/setup.sh --day2
```

Run a live demo directly:
```bash
python3 demos/day1/beat_1_1_variables.py
python3 demos/day2/beat_2_1_functions.py
```

Run the automated checks:
```bash
python3 -m unittest discover -s exercises/tests -v
```

Reset generated demo files:
```bash
scripts/setup.sh --reset
```

## Layout
```
README.md                 Course overview & Day 1 / Day 2 entry points
instructor-steps.md       Quick instructor reference for class day
course/
  modules/                Beat-by-beat teaching scripts (01-python-i.md, 02-python-ii.md)
  slides/                 Teaching slide decks (day1-python-i-slides.md, day2-python-ii-slides.md)
demos/
  day1/                   Runnable terminal demos for Day 1 (Beats 1.1–1.5)
  day2/                   Runnable terminal demos for Day 2 (Beats 2.1–2.4) + sample data/
exercises/                Day 1 & Day 2 student starter scripts + tests/
scripts/
  setup.sh                Prerequisite checks + demo verification (--day1, --day2, --reset)
  smoke.sh                Runs and verifies every Day 1 and Day 2 demo
.claude/skills/           setup-python-class, teach-python-class (instructors);
                          setup-candidate, practice-python (students)
docs/                     Course TOC, instructor guide, quick start, student guide
```

