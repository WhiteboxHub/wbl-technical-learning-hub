# Week 2 PM — Production ML & MLOps Table of Contents

Whitebox Learning — Agentic AI Engineering (Week 2 PM).
Running project: **MLOps Fraud Detection System** (`fraud_system/`).
Reference presentation: `MLops` (222-page PDF deck).

> Note: There are no invented numeric pass thresholds anywhere in this program. Every gate is a demonstrable outcome.

## Week Overview & Slide Deck Alignment

| Day | Session | Story Anchor | `MLops` PDF Slides | Slide Gaps / Notes |
|---|---|---|---|---|
| **Mon** | ML Lifecycle + MLflow Experiment Tracking | *The lab notebook* | `1–22`, `58–71`, `77–88`, `102–106`, `116–118`, `120`, `126–127`, `140`, `146–149` | Update MLflow `transition_model_version_stage` (`88`, `149`) alongside aliases `@champion`/`@challenger` (`118`) |
| **Tue** | DVC + Data and Pipeline Versioning | *The time machine for data* | `30`, `56–57`, `102`, `105`, `218–219` (partial mentions only) | **Gap:** No dedicated DVC command/pipeline slides; teach from `5A` material & `demos/tue_*.py` |
| **Wed** | Model Deployment — FastAPI + Docker | *The restaurant opens* | `150–172` | Add `/health`, `/v1/` endpoint versioning, and rollback mechanics via `5A` + `serve.py` |
| **Thu** | Monitoring + Drift Detection | *The lighthouse keeper* | `173–221` (49 slides in PDF!) | Guide notes partial website coverage, but attached PDF covers drift, Evidently, Prometheus, alerting & retraining in depth |
| **Fri** | Worked Template Build — Fraud Detection | *All 4 anchors in one system* | Synthesis across `1–221` | Built in-class across AM + PM; overflow rule applies over weekend |
| **Wknd** | No class — Instructor follow-up only | — | — | Candidate closed-book self-test + optional agent catch-up |

## Day-by-Day Module Files
1. [Monday: ML Lifecycle + MLflow Experiment Tracking](../course/modules/01-monday-ml-lifecycle-mlflow.md)
2. [Tuesday: DVC + Data and Pipeline Versioning](../course/modules/02-tuesday-dvc-versioning.md)
3. [Wednesday: Model Deployment — FastAPI + Docker](../course/modules/03-wednesday-deployment-fastapi-docker.md)
4. [Thursday: Monitoring + Drift Detection](../course/modules/04-thursday-monitoring-drift.md)
5. [Friday: Worked Template Build — Fraud Detection](../course/modules/05-friday-fraud-template-build.md)
6. [Weekend: Instructor Follow-Up, Self-Test & Exit Gate](../course/modules/06-weekend-followup-selftest.md)
7. [Candidate Evening Rhythm & Prompts](../course/candidate-prompts.md)
