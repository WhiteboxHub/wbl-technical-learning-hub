---
name: setup-candidate
description: Candidate (student) setup for the Python I & Python II (AI Engineering Edition) course. Use when a student wants to get their laptop ready, says "set up my environment", "Python isn't working", or needs to reset their demo files. Checks Python 3.10+, verifies Day 1 and Day 2 demos, and guides them through running their first Python script.
---

# Candidate setup

Get a beginner learner from a fresh laptop to running their first Python AI demo cleanly. Be friendly and concrete; assume they may be brand new to Python and the terminal. Explain what each step does in one short sentence before running it.

## Steps

1. **Run `bash scripts/setup.sh`** from the `python-course` root (or `bash scripts/setup.sh --day1` / `--day2` for a single day).
2. **If it fails, use the exit code:**

| Exit | Say this, then |
|---|---|
| 10 | "`python3` isn't installed yet." Give the https://www.python.org/downloads/ link. Do not install software without their permission. |
| 11 | "Your Python version is older than 3.10." Show the detected version and ask them to install Python 3.10+. |
| 12 | "Some course files are missing." Show which file was missing and confirm they are inside `python-course/`. |
| 13 | "One of the demo checks failed." Show the FAIL lines, explain in plain words, and fix/reset safely. |

   On Windows, note that `.sh` scripts need Git Bash or WSL2, or they can run `python --version` and `python demos/day1/beat_1_1_variables.py` directly in PowerShell.
3. **First Python run, together.** Once it says **READY**, have them run and explain the output:
   ```bash
   python3 demos/day1/beat_1_1_variables.py
   ```
   Point out how Python ran top to bottom, printed the initial `gpt-4o-mini` variable, and then printed `gemini-2.5-flash` after reassignment.
4. **Confirm and wrap up** with where Day 1 (`exercises/day1_exercise.py`) and Day 2 (`exercises/day2_exercise.py`) exercises live, and how to reset demo files (`bash scripts/setup.sh --reset`).

## Rules
- Never solve issues silently: say what failed and what you changed.
- Do not edit course modules or finish exercises during setup.
- If they ask about Python syntax or class concepts, point them to `practice-python` ("quiz me" / "explain ...") after setup finishes.

