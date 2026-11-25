# Week 2 Day 1 AM: Statistics & Probability for ML

Reference repository formatted after the `http-course-main` course structure, containing the curriculum, runnable demos, universal multi-agent AI skill, automated verification scripts, and documentation for **Week 2 Day 1 Morning (AM)** of the Whitebox Learning Agentic AI Engineering program.

- **Story Anchor:** *The weather forecaster who is never certain, only honest about the odds.*
- **Core Premise:** A forecast of "70% chance of rain" is an honest statement about uncertainty, not a broken promise when it stays sunny 3 out of 10 times. Machine learning models produce probability distributions, not certainties; without understanding distributions, base rates, and sampling bias, models fail in production.

---

## Quick Start (1 Command)

```bash
scripts/setup.sh
```

This script:
1. Verifies Python 3.10+
2. Verifies environment and dependencies (`numpy`)
3. Verifies starter datasets in `data/`
4. Executes the automated smoke test suite (`scripts/smoke.sh`)

To run all morning demos in sequence:
```bash
bash demos/run_all.sh
```

---

## Universal Multi-Agent Skill (`stats-skill`)

Instead of maintaining redundant, fragmented prompts across multiple directories, this repository provides a **single canonical Universal Skill Prompt** compatible across all major LLMs and coding agents:

- **Canonical Definition:** [`skills/stats-skill/SKILL.md`](skills/stats-skill/SKILL.md)
- **Universal Agent Context:** [`AGENTS.md`](AGENTS.md)
- **Web & Chat Master Prompt:** [`docs/agent-prompts.md`](docs/agent-prompts.md)

### Supported Agent Platforms

| Agent Platform | Configuration Link | How to Trigger |
|---|---|---|
| **Claude Code** | `.claude/skills/stats-skill` | Run `claude`, then say `"teach stats"` or `"quiz me on stats"` |
| **Google Antigravity & Gemini CLI** | `skills/stats-skill/SKILL.md` & `AGENTS.md` | Say `"teach stats"`, `"practice stats"`, or `"verify setup"` |
| **OpenAI Codex & Universal Agents** | `skills/stats-skill/SKILL.md` & `AGENTS.md` | Auto-loaded by agent runners from workspace root |
| **Cursor IDE** | `skills/stats-skill/SKILL.md` & `AGENTS.md` | Auto-indexed rules applied in Composer and Chat |
| **Web LLMs (ChatGPT, Claude Web, Grok)** | `docs/agent-prompts.md` | Single copy-pasteable master prompt for web chats |

### Dynamic Modes (Zero Redundancy)

The universal skill automatically adapts based on what you ask:
- **Instructor Co-Pilot:** Triggered by `"teach stats"`, `"start class"`, `"next beat"`. Walks beats 1.1–1.7, holds check question answers, updates `.class/progress.md`.
- **Socratic Practice Coach:** Triggered by `"quiz me on stats"`, `"practice stats"`, `"check my answer"`. Quizzes 1-at-a-time, climbs 4-rung hint ladder, verifies outputs.
- **Environment Setup:** Triggered by `"set up environment"`, `"verify my laptop"`. Tests Python, NumPy, datasets, and runs smoke tests.
- **Candidate Assessment:** Triggered by `"done-check"`, `"self-check"`. Evaluates the 5 exit questions and updates `candidate-state.md`.

---

## Morning Curriculum & Demos

| Beat | Title | Demo Script | Concept Demonstrated |
|---|---|---|---|
| **Beat 1.1** | The Weather Forecaster | — | Uncertainty, probabilistic thinking, model output scores |
| **Beat 1.2** | Reading Data Shapes | `python3 demos/demo1_distributions.py --samples 500` | Normal vs Skewed vs Heavy-tailed; why mean lies when tails are heavy |
| **Beat 1.3** | Spread & Outliers | `python3 demos/demo1_distributions.py --outlier 500.0` | Mean vs Median; variance, standard deviation, IQR, outlier sensitivity |
| **Beat 1.4** | Bayes' Theorem | `python3 demos/demo2_bayes_calculator.py` | 10,000-person grid; base rate neglect; natural frequency counts |
| **Beat 1.5** | Sampling Bias | `python3 demos/demo3_sampling_bias.py` | 20,000 voluntary survey respondents (biased) vs 500 random sample |
| **Beat 1.6** | Signal vs Noise | `python3 demos/demo3_sampling_bias.py` | A/B testing: $n=2,000$ vs $n=20,000$ statistical significance |
| **Beat 1.7** | Hands-On Exercise | `python3 demos/demo2_bayes_calculator.py --prevalence 0.05` | Custom Bayes sensitivity drill & Done-check rubric |

---

## Core Documentation

- [Class-Day Quick Start](docs/class-day-quickstart.md) — 5-minute instructor launch checklist
- [Instructor Steps](instructor-steps.md) — Step-by-step instructor operational run sheet
- [Instructor Guide](docs/instructor-guide.md) — In-depth instructor reference manual and exit check rubric
- [Student Guide](docs/student-guide.md) — Candidate study guide, cheat sheets, exercises, and self-checks
- [Course Table of Contents](docs/course-toc.md) — Detailed syllabus and roadmap
- [Universal Agent Prompts](docs/agent-prompts.md) — Master prompt for ChatGPT, Claude Web, and Grok
- [Candidate State Tracker](candidate-state.md) — Candidate progress record

---

## Repository Layout

```
├── README.md                                  # Repository overview and quick start
├── AGENTS.md                                  # Universal coding agent instructions
├── instructor-steps.md                        # Step-by-step instructor run sheet
├── candidate-state.md                         # Standardized candidate progress tracker
├── requirements.txt                           # Python dependencies (numpy, scipy, matplotlib)
├── docker-compose.yml                         # Containerized Python stats environment
├── .class/
│   └── progress.md                            # In-class progress log
├── skills/
│   └── stats-skill/
│       └── SKILL.md                           # CANONICAL UNIVERSAL SKILL PROMPT
├── .claude/skills/                            # Symlinked to skills/stats-skill
├── course/modules/
│   └── 01-statistics-and-probability.md       # Primary curriculum beats 1.1 - 1.7
├── docs/
│   ├── class-day-quickstart.md                # 5-minute teaching launch guide
│   ├── instructor-guide.md                    # In-depth instructor reference manual
│   ├── student-guide.md                       # Candidate study guide & exercises
│   ├── course-toc.md                          # Curriculum table of contents
│   └── agent-prompts.md                       # Multi-agent prompt catalog
├── scripts/
│   ├── setup.sh                               # One-command setup script
│   ├── smoke.sh                               # Automated verification suite
│   └── reset.sh                               # State and cache reset utility
├── demos/
│   ├── run_all.sh                             # All-in-one demo runner
│   ├── demo1_distributions.py                 # Distributions, skewness & spread demo
│   ├── demo2_bayes_calculator.py              # Bayes theorem & natural counts demo
│   └── demo3_sampling_bias.py                 # Sampling bias & signal vs noise demo
└── data/
    ├── medical_screening_sample.csv           # 10,000-row Bayes screening dataset
    └── weather_forecaster_survey.csv          # Survey bias demonstration dataset
```
