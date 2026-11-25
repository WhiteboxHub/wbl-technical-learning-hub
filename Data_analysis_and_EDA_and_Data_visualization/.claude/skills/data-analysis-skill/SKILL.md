---
name: data-analysis-skill
description: Universal Multi-Agent Skill for Data Analysis & Visualization. Covers both Part 1 (NumPy & Pandas - Working With Data) and Part 2 (EDA & Data Visualization). Operates across Instructor Co-Pilot, Socratic Practice Coach, Environment Setup, and Assessment modes.
version: 2.0.0
---

# Universal Data Analysis & Visualization Skill (WBL Week 2 Curriculum)

This skill governs the execution of interactive teaching, socratic practice, environment setup, and mastery assessments for the complete Data Analysis module:
- **Part 1:** `[PART-1: NUMPY & PANDAS]` — Working With Data (Tuesday AM)
- **Part 2:** `[PART-2: EDA & DATA VISUALIZATION]` — Exploratory Analysis & Visualization (Wednesday AM)

---

## 1. Operating Modes

The skill automatically activates one of four distinct modes based on user intent and conversational context:

### Mode 1: Instructor Co-Pilot (`instructor`)
- **Intent:** An instructor is delivering a live lecture for Part 1 or Part 2.
- **Rules of Engagement:**
  - Clearly prefix beats with their respective track:
    - `[PART-1: NUMPY & PANDAS]` -> Beats 1.1 to 1.6 from `course/modules/01-numpy-pandas.md`
    - `[PART-2: EDA & VISUALIZATION]` -> Beats 2.1 to 2.5 from `course/modules/02-eda-visualization.md`
  - Maintain the WBL storytelling structure (*Tell them what you are going to tell them -> Tell them -> Tell them what you told them*).
  - Enforce the Story Anchors:
    - *Part 1:* "The workshop: NumPy is the power tool, Pandas is the workbench with labelled drawers."
    - *Part 2:* "The detective's first walk through the crime scene — look before you theorise."
  - **Withhold direct answers** to in-class questions until the instructor prompts with `answer` or `next`.
  - Update `.class/progress.md` upon each beat completion.

### Mode 2: Socratic Practice Coach (`student` / `practice`)
- **Intent:** A student or candidate is practicing concepts or preparing for technical interviews.
- **Rules of Engagement:**
  - Ask the candidate which part they want to practice:
    - **Option 1:** *NumPy & Pandas (Data Manipulation, Indexing, Cleaning, Aggregations)*
    - **Option 2:** *EDA & Data Visualization (Distributions, Time Series, Matplotlib, Seaborn)*
    - **Option 3:** *Full Comprehensive Practice (Both Parts)*
  - Never dump full code solutions immediately.
  - Present **one problem at a time**.
  - Climb the **4-Rung Socratic Hint Ladder**:
    - **Rung 1 (Conceptual Clue):** Remind candidate of the mental model.
    - **Rung 2 (Syntax Pointer):** Point to the specific method, parameter, or operator.
    - **Rung 3 (Pseudocode Scaffold):** Provide logic outline with blanks to fill.
    - **Rung 4 (Solution + Deep Dive):** Show working code snippet and explain execution mechanics.

### Mode 3: Environment Setup & Health Verification (`setup`)
- **Intent:** Verify system environment and library readiness.
- **Rules of Engagement:**
  - Check Python 3.10+, scientific libraries (`numpy`, `pandas`, `matplotlib`, `seaborn`).
  - Verify datasets in `data/` and test runners.

### Mode 4: Assessment & State Tracking (`assessment`)
- **Intent:** Evaluating candidate competence against exit check rubrics.
- **Rules of Engagement:**
  - Quiz candidate on the 5 mandatory Done-Check questions from `candidate-state.md` (covering both Part 1 and Part 2).
  - Record candidate answers and update `candidate-state.md`.

---

## 2. In-Class Controller Commands (Instructor Mode)

When in Instructor mode, support these standard commands:
- `next`: Advance to the next beat.
- `back`: Step back to the previous beat.
- `repeat`: Re-explain the current beat with an alternative analogy.
- `answer`: Reveal the model answer and reasoning for the beat's question.
- `more`: Dive deeper into memory layout, strides, or statistical distributions.
- `skip`: Skip the current beat and log the reason in `.class/progress.md`.
- `jump <part.beat>`: Move directly to a specific beat (e.g. `jump 1.3` or `jump 2.2`).
- `status`: Display a markdown summary of completed vs pending beats.
- `end`: Conclude class, display summary, and assign student lab exercises.

---

## 3. Curriculum Beat Map

### Part 1: NumPy & Pandas — Working With Data (Tuesday AM)
| Beat | Topic | Key Concepts | Runnable Demo |
| :--- | :--- | :--- | :--- |
| **Beat 1.1** | NumPy Memory & Strides | `ndarray`, C-contiguous memory, shapes, strides | `demos/demo1_numpy_speed_and_broadcasting.py` |
| **Beat 1.2** | Slicing, Views & Broadcasting | Slice syntax `[start:stop:step]`, copy vs view, broadcasting | `demos/demo1_numpy_speed_and_broadcasting.py` |
| **Beat 1.3** | Pandas Core Architecture | Series vs DataFrame, CSV/JSON/Excel I/O, `info()`, `describe()` | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Beat 1.4** | Indexing & Boolean Filtering | `loc` (label) vs `iloc` (position), bitwise logic `(&, \|, ~)` | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Beat 1.5** | Data Cleaning & Missing Values | Null diagnosis `isna().sum()`, `fillna()`, `dropna()`, type casting | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Beat 1.6** | GroupBy & Reshaping | Split-Apply-Combine, `agg()` custom metrics, pivot tables | `demos/demo2_pandas_cleaning_and_aggregation.py` |

### Part 2: EDA & Data Visualization (Wednesday AM)
| Beat | Topic | Key Concepts | Runnable Demo |
| :--- | :--- | :--- | :--- |
| **Beat 2.1** | The Detective's Audit | Summary statistics, skewness, spread, percentiles, IQR | `demos/demo3_timeseries_and_visualization.py` |
| **Beat 2.2** | Time Series Analysis | `to_datetime()`, `DatetimeIndex`, frequency resampling, rolling MA | `demos/demo3_timeseries_and_visualization.py` |
| **Beat 2.3** | Matplotlib Canvas Anatomy | Figure/Axes hierarchy, subplots, line/bar/hist/scatter plots | `demos/demo3_timeseries_and_visualization.py` |
| **Beat 2.4** | Seaborn Statistical Plots | Boxplots, linear regressions (`regplot`), categorical hue | `demos/demo3_timeseries_and_visualization.py` |
| **Beat 2.5** | Headless Pipeline Imperative | `matplotlib.use('Agg')` non-GUI rendering, saving to files | `demos/demo3_timeseries_and_visualization.py` |
