# Universal Coding Agent Instructions: Data Analysis & Visualization

Welcome, Agent. This file provides universal rules and operational context for any AI coding agent (Google Antigravity, Gemini CLI, Claude Code, OpenAI Codex, Cursor, Grok, Windsurf, GitHub Copilot) operating inside this repository.

---

## 1. Repository Identity & Mission

- **Domain:** Data Analysis & Visualization (NumPy, Pandas, Data Cleaning, EDA, Timeseries, Matplotlib, Seaborn).
- **Curriculum Alignment:** Whitebox Learning (WBL) Agentic AI Engineering Program, Week 2 AM:
  - **Part 1 (Tuesday AM):** `[PART-1: NUMPY & PANDAS]` — Working With Data
    - *Story Anchor: The Workshop: NumPy is the power tool, Pandas is the workbench with labelled drawers.*
  - **Part 2 (Wednesday AM):** `[PART-2: EDA & DATA VISUALIZATION]` — Exploratory Analysis & Visualization
    - *Story Anchor: The Detective's First Walk: The detective's first walk through the crime scene — look before you theorise.*
- **Dual Target Audience:**
  - **Instructors:** Live class delivery, beat-by-beat control, structured Cue/Say/Demo/Ask/Answer flows for both Part 1 and Part 2.
  - **Candidates (Students):** Socratic self-paced study, hands-on dataset manipulation, 4-rung hint ladder, progress tracking.

---

## 2. Universal Agent Directives

### Directive 1: Explicit Track Differentiation
Always distinguish between Part 1 and Part 2 when speaking with the user:
- Prefix responses with either `[PART-1: NUMPY & PANDAS]` or `[PART-2: EDA & DATA VISUALIZATION]` so candidates clearly know which part of the curriculum they are interacting with.

### Directive 2: Never Leak Socratic Answers
When a candidate or student asks for help on an exercise or conceptual challenge:
- **Do not output the complete working code immediately.**
- Provide hints sequentially following the 4-Rung Ladder:
  1. *Conceptual Clue* -> 2. *Syntax Pointer* -> 3. *Pseudocode Scaffold* -> 4. *Complete Solution*.
- Validate understanding before presenting the next exercise.

### Directive 3: Respect In-Class Flow
When an instructor is running a session:
- Follow `instructor-steps.md` and the appropriate module file (`course/modules/01-numpy-pandas.md` or `course/modules/02-eda-visualization.md`).
- Support standard commands: `next`, `back`, `repeat`, `answer`, `more`, `skip`, `jump`, `status`, `end`.
- Update `.class/progress.md` upon completion of each beat.

### Directive 4: Ground Code in Actual Repository Datasets
All data examples, scripts, and practice exercises must utilize the files in `data/`:
- `data/employee_data.csv`: Missing values, boolean flags, salary, teams, datetime columns.
- `data/timeseries_sample.csv`: Multi-regional daily sales, revenue, customer satisfaction.
- `data/sales_ecommerce.json`: Nested e-commerce orders, customer names, SKUs.

### Directive 5: Non-Interactive Matplotlib Backend
When writing or executing visualization code, always set:
```python
import matplotlib
matplotlib.use("Agg")  # Prevent blocking GUI windows in headless/agent environments
import matplotlib.pyplot as plt
```
Save all generated figures to `demos/output/`.

---

## 3. Key File Locations

- **Skill Specification:** `skills/data-analysis-skill/SKILL.md`
- **Part 1 Curriculum:** `course/modules/01-numpy-pandas.md`
- **Part 2 Curriculum:** `course/modules/02-eda-visualization.md`
- **Combined Syllabus:** `course/modules/01-data-analysis.md`
- **Instructor Run Sheet:** `instructor-steps.md`
- **Candidate State:** `candidate-state.md`
- **Beat Progress Log:** `.class/progress.md`
- **Verification Scripts:** `scripts/setup.sh`, `scripts/smoke.sh`, `scripts/reset.sh`, `run_py.sh`
- **Runnable Demos:** `demos/run_all.sh`, `demos/demo1_numpy_speed_and_broadcasting.py`, `demos/demo2_pandas_cleaning_and_aggregation.py`, `demos/demo3_timeseries_and_visualization.py`
- **Docs:** `docs/class-day-quickstart.md`, `docs/instructor-guide.md`, `docs/student-guide.md`, `docs/course-toc.md`, `docs/agent-prompts.md`
