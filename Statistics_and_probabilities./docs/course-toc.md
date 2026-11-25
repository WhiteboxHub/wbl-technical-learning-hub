# Course Table of Contents: Week 2 Day 1 AM
# Statistics & Probability for ML

Comprehensive curriculum syllabus and roadmap for **Week 2 Day 1 Morning (AM)** of the Whitebox Learning Agentic AI Engineering program.

---

## Week 2 Program Overview

| Day | Morning Session (AM) | Afternoon Session (PM) |
|---|---|---|
| **Monday (Day 1)** | **Statistics & Probability for ML** (This Repository) | ML Lifecycle + MLflow Experiment Tracking |
| **Tuesday (Day 2)** | NumPy & Vectorized Computation | DVC, Data Versioning & S3 Storage |
| **Wednesday (Day 3)** | Pandas & Feature Engineering | Scikit-learn Pipelines & Feature Stores |
| **Thursday (Day 4)** | Supervised Learning & Loss Functions | Model Evaluation, Drift & Calibration |
| **Friday (Day 5)** | Capstone Project: End-to-End Pipeline | Final Review & Production Deployment |

---

## Week 2 Day 1 AM: Statistics & Probability for ML

- **Skill Identifier:** `stats-skill` / `skills/stats-skill/SKILL.md`
- **Story Anchor:** *The weather forecaster who is never certain, only honest about the odds.*
- **Estimated Duration:** 3 hours (7 lesson beats, 3 runnable demos, 2 datasets)

### Detailed Beat Breakdown

#### Beat 1.1: The Weather Forecaster & Uncertainty
- Probabilistic vs deterministic thinking
- Probability distributions as statements of uncertainty
- The risk of treating model scores as binary truths

#### Beat 1.2: Reading the Shape of Data
- Normal (Gaussian) distributions and symmetry
- Right-skewed distributions and financial/operational data
- Heavy-tailed (Power law / Pareto) distributions and tail risk
- **Demo:** `demos/demo1_distributions.py --samples 500`

#### Beat 1.3: Spread: Why the Mean Lies
- Mean as center of gravity vs Median as typical value
- Variance, Standard Deviation, and Interquartile Range (IQR)
- Outlier injection and breakdown points
- **Demo:** `demos/demo1_distributions.py --outlier 500.0`

#### Beat 1.4: Conditional Probability & Bayes' Theorem
- Joint probability $\mathbb{P}(A \cap B)$ vs Conditional probability $\mathbb{P}(A \mid B)$
- Bayes' Theorem formulation and prior updating
- Base rate fallacy and 10,000-person natural frequency counts
- **Demo:** `demos/demo2_bayes_calculator.py`

#### Beat 1.5: Sampling Bias: Size Does Not Fix Bias
- Selection bias, non-response bias, and survivorship bias
- Why 20,000 voluntary survey responses fail compared to 500 random ones
- Sample data verification: `data/weather_forecaster_survey.csv`
- **Demo:** `demos/demo3_sampling_bias.py` (Part 1)

#### Beat 1.6: Hypothesis Thinking: Signal vs Noise
- Sampling distributions and standard error
- A/B testing: evaluating observed lift against random variance
- Sample size requirements: $n=2,000$ vs $n=20,000$
- **Demo:** `demos/demo3_sampling_bias.py` (Part 2)

#### Beat 1.7: Hands-On Exercise & Done-Check
- Independent Bayes simulation drills
- Candidate self-check questions and evaluation rubric
- Logging outcomes in `candidate-state.md`

---

## Repository Files & Assets

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
