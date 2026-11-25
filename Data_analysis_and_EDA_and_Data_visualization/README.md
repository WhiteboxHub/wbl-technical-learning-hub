# Data Analysis & Visualization Repository

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Curriculum: WBL Week 2 AM](https://img.shields.io/badge/Curriculum-WBL%20Week%202%20AM-orange.svg)]()
[![Multi-Agent: Universal](https://img.shields.io/badge/Agents-Antigravity%20%7C%20Claude%20%7C%20Cursor%20%7C%20Codex-purple.svg)]()

> **Story Anchors:**  
> - **Part 1:** *The Workshop:* NumPy is the power tool, Pandas is the workbench with labelled drawers.  
> - **Part 2:** *The Detective's First Walk:* The detective's first walk through the crime scene — look before you theorise.

A dual-purpose, production-grade learning and teaching repository designed for **candidates (students)** and **instructors** in the Whitebox Learning (WBL) Agentic AI Engineering Program. This repository houses **two unified modules under one roof**:

1. `[PART-1: NUMPY & PANDAS]` — Working With Data (Tuesday AM)
2. `[PART-2: EDA & DATA VISUALIZATION]` — Exploratory Analysis & Visualization (Wednesday AM)

---

## Quick Start (Under 60 Seconds)

```bash
# Clone and enter directory
cd Data_analysis

# Automated environment setup & dependency check
bash scripts/setup.sh

# Run end-to-end smoke tests
bash scripts/smoke.sh

# Execute all runnable demos
bash demos/run_all.sh

# Or run individual scripts with the environment helper
./run_py.sh demos/demo1_numpy_speed_and_broadcasting.py
./run_py.sh demos/demo2_pandas_cleaning_and_aggregation.py
./run_py.sh demos/demo3_timeseries_and_visualization.py
```

---

## Dual-Module Structure & Curriculum Matrix

```
┌───────────────────────────────────────────────────────────────────────────────────────┐
│                               DATA ANALYSIS REPOSITORY                                │
├───────────────────────────────────────────┬───────────────────────────────────────────┤
│    PART 1: NUMPY & PANDAS                 │    PART 2: EDA & DATA VISUALIZATION       │
│    (Tuesday AM — Working With Data)       │    (Wednesday AM — The Detective's Walk)  │
├───────────────────────────────────────────┼───────────────────────────────────────────┤
│ • Memory layout, strides & SIMD speed     │ • Summary stats, percentiles & skewness   │
│ • Slicing views vs explicit copies        │ • Temporal intelligence & frequency       │
│ • Broadcasting across dimensions          │ • Rolling window moving averages (trend)  │
│ • Positional (iloc) vs Label (loc)        │ • Matplotlib Object-Oriented anatomy      │
│ • Boolean masking & bitwise filters       │ • Seaborn boxplots & linear regressions   │
│ • Missing data diagnosis & imputation     │ • Headless pipelines (matplotlib.use)     │
│ • Split-Apply-Combine & GroupBy agg       │ • Output: High-res dashboard charts       │
└───────────────────────────────────────────┴───────────────────────────────────────────┘
```

| Module | Beat | Topic | Key Concepts | Runnable Demo |
| :---: | :---: | :--- | :--- | :--- |
| **Part 1** | **Beat 1.1** | NumPy Memory & Strides | `ndarray`, contiguous memory, strides, shape metadata | `demos/demo1_numpy_speed_and_broadcasting.py` |
| **Part 1** | **Beat 1.2** | Slicing, Views & Broadcasting | Slice syntax `[start:stop:step]`, view trap, broadcasting rules | `demos/demo1_numpy_speed_and_broadcasting.py` |
| **Part 1** | **Beat 1.3** | Pandas Core Architecture | Series vs DataFrame, multi-format I/O, `.info()`, `.describe()` | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Part 1** | **Beat 1.4** | Indexing & Boolean Filtering | `loc` (label/condition) vs `iloc` (position), bitwise logic `(&, \|, ~)` | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Part 1** | **Beat 1.5** | Data Cleaning & Missing Values | Null diagnosis `.isna().sum()`, `fillna()`, `dropna()`, type casting | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Part 1** | **Beat 1.6** | GroupBy & Reshaping | Split-Apply-Combine, custom metrics `.agg()`, pivot tables | `demos/demo2_pandas_cleaning_and_aggregation.py` |
| **Part 2** | **Beat 2.1** | The Detective's Audit | Summary statistics, spread, percentiles, IQR, skewness | `demos/demo3_timeseries_and_visualization.py` |
| **Part 2** | **Beat 2.2** | Time Series Analysis | DatetimeIndex, frequency resampling (`resample`), rolling MA | `demos/demo3_timeseries_and_visualization.py` |
| **Part 2** | **Beat 2.3** | Matplotlib Canvas Anatomy | Figure/Axes hierarchy, subplots, line/bar/hist/scatter plots | `demos/demo3_timeseries_and_visualization.py` |
| **Part 2** | **Beat 2.4** | Seaborn Statistical Plots | Boxplots across categories, regression plots (`regplot`), hue | `demos/demo3_timeseries_and_visualization.py` |
| **Part 2** | **Beat 2.5** | Headless Pipeline Imperative | `matplotlib.use('Agg')` non-GUI rendering, saving figures | `demos/demo3_timeseries_and_visualization.py` |

---

## Universal Multi-Agent Skills Support

This repository is equipped with a canonical agent skill (`skills/data-analysis-skill/SKILL.md`) that works across all major AI coding agents:

| AI Agent Platform | Skill Entry Path | Activation Command / Prompt |
| :--- | :--- | :--- |
| **Google Antigravity / Gemini CLI** | `skills/data-analysis-skill/SKILL.md` | *"Activate data-analysis-skill for Part 1 in Instructor Mode"* |
| **Claude Code** | `.claude/skills/data-analysis-skill/SKILL.md` | `claude "Follow AGENTS.md and quiz me on Part 2 EDA"` |
| **Cursor / Codex / Windsurf** | `.agent/skills/data-analysis-skill/` | *"Act as Socratic Practice Coach using candidate-state.md"* |
| **Docker Container** | `docker-compose.yml` | `docker-compose up --build` |

---

## Core Documentation & Guides

- [course/modules/01-numpy-pandas.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/course/modules/01-numpy-pandas.md) — Part 1 curriculum: NumPy & Pandas.
- [course/modules/02-eda-visualization.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/course/modules/02-eda-visualization.md) — Part 2 curriculum: EDA & Data Visualization.
- [instructor-steps.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/instructor-steps.md) — In-class run sheet for both Tuesday AM and Wednesday AM sessions.
- [candidate-state.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/candidate-state.md) — Comprehensive candidate progress tracker with 5 exit Done-Check questions.
- [docs/class-day-quickstart.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/docs/class-day-quickstart.md) — 5-minute pre-class checklist for instructors.
- [docs/instructor-guide.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/docs/instructor-guide.md) — Detailed pedagogical strategies, common pitfalls, and grading rubrics.
- [docs/student-guide.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/docs/student-guide.md) — Candidate mental models, cheatsheets, and hands-on lab exercises.
- [docs/course-toc.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/docs/course-toc.md) — Visual curriculum roadmap.
- [docs/agent-prompts.md](file:///Users/hrinnova-path.com/Desktop/GUIDES/Data_analysis/docs/agent-prompts.md) — Ready-to-use prompts for LLM coding agents.

---

## Repository Directory Layout

```
Data_analysis/
├── README.md                           # Main repository landing page & documentation
├── AGENTS.md                           # Universal agent operational directives
├── instructor-steps.md                 # Live lecture run sheet for Part 1 & Part 2
├── candidate-state.md                  # Standardized candidate progress tracker & exit checks
├── run_py.sh                           # Lightweight python runner helper
├── requirements.txt                    # Minimal scientific dependencies
├── docker-compose.yml                  # Containerized execution environment
├── .gitignore                          # Standard Python & OS ignore rules
├── .class/
│   └── progress.md                     # Live in-class beat status tracker for Part 1 & 2
├── skills/
│   └── data-analysis-skill/
│       └── SKILL.md                    # Universal multi-agent skill specification
├── course/
│   └── modules/
│       ├── 01-data-analysis.md         # Combined curriculum overview
│       ├── 01-numpy-pandas.md          # Part 1 curriculum: NumPy & Pandas
│       └── 02-eda-visualization.md     # Part 2 curriculum: EDA & Data Visualization
├── data/
│   ├── employee_data.csv               # Dirty HR dataset with missing values & datetimes
│   ├── timeseries_sample.csv           # Multi-regional daily sales & satisfaction metrics
│   └── sales_ecommerce.json            # Nested customer orders and product SKUs
├── demos/
│   ├── run_all.sh                      # Shell script executing all three demos
│   ├── demo1_numpy_speed_and_broadcasting.py # Memory strides, vectorization benchmark, views
│   ├── demo2_pandas_cleaning_and_aggregation.py # Data cleaning, indexing, GroupBy & pivots
│   ├── demo3_timeseries_and_visualization.py   # Timeseries resampling, rolling MA, Matplotlib + Seaborn
│   └── output/                         # Generated high-resolution dashboards and charts
├── docs/
│   ├── class-day-quickstart.md         # 5-minute pre-class instructor checklist
│   ├── instructor-guide.md             # In-depth pedagogical advice & pitfall interventions
│   ├── student-guide.md                # Study guide, cheatsheets, and lab exercises
│   ├── course-toc.md                   # Visual curriculum map and syllabus
│   └── agent-prompts.md                # Ready-to-use prompts for LLM coding agents
└── scripts/
    ├── setup.sh                        # Environment bootstrap & dependency validator
    ├── smoke.sh                        # Automated test runner verifying imports, demos, datasets
    └── reset.sh                        # Clean build outputs, caches, and reset progress
```

---

## License

This repository is maintained for the Whitebox Learning (WBL) Agentic AI Engineering curriculum. Distributed under the MIT License.
