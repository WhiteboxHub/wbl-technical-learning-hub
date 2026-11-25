---
name: setup-python-class
description: Instructor setup for the Python I & Python II (AI Engineering Edition) course. Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or wants to verify Day 1 / Day 2 Python demos. Checks Python 3.10+, verifies course files and exercises, runs the smoke test, and reports readiness.
---

# Instructor setup

Gets the instructor's machine ready to teach Day 1 or Day 2. The work is done by `scripts/setup.sh`; your job is to run it, interpret the result, and fix what you safely can.

## Steps

1. **Run the setup script** from the `python-course` root:
   - Full check (Day 1 & Day 2): `bash scripts/setup.sh`
   - Or single day: `bash scripts/setup.sh --day1` / `bash scripts/setup.sh --day2`
2. **Handle the exit code:**

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Go to step 3 |
| 10 | `python3` missing | Tell the instructor to install Python 3.10+ from https://www.python.org/downloads/. Do not install it without asking. |
| 11 | Python version < 3.10 | Report the detected version and ask the instructor to upgrade to Python 3.10+. |
| 12 | Missing course files | Check which expected file in `course/`, `demos/`, or `exercises/` is missing and report clearly. |
| 13 | Smoke test failed | Show the FAIL lines, inspect the failing script in `demos/` or `exercises/tests/test_demos.py`, fix or reset, and re-run. |

3. **Check the teaching environment** (report each as ready or missing; do not invent missing items):
   - `docs/course-toc.md` exists
   - Day 1 module & slides exist (`course/modules/01-python-i.md`, `course/slides/day1-python-i-slides.md`)
   - Day 2 module & slides exist (`course/modules/02-python-ii.md`, `course/slides/day2-python-ii-slides.md`)
   - First demo runs cleanly: `python3 demos/day1/beat_1_1_variables.py`
   - Unit verification passes: `python3 -m unittest discover -s exercises/tests -v`
4. **Report a short readiness checklist**, showing how to start Day 1 (`teach day 1`), Day 2 (`teach day 2`), and how to clean up generated demo output (`scripts/setup.sh --reset`).
5. **Point to the next step:** the instructor can say **"teach day 1"** or **"teach day 2"** to launch `teach-python-class`.

## Rules
- Idempotent: running again on a healthy setup is safe and quick.
- `--reset` only removes generated demo output files (`demos/day2/data/run_log.txt`, `demos/day2/data/updated_config.json`); it does not touch `.class/progress.md` or student edits.
- Do not modify course modules, demos, or exercises silently just to make setup pass without telling the instructor what and why.

