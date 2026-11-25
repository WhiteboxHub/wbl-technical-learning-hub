# Student Guide — Week 2 PM Production ML

Welcome to **Week 2 PM: Production ML & MLOps**. Every task in this course runs **locally on your laptop** (CoderPad has no candidate-facing entry point on the site).

---

## 1. What You Will Build
Across Monday–Friday, you will assemble a working **MLOps Fraud Detection System**:
- **Monday:** Track experiments and register models in **MLflow**.
- **Tuesday:** Version datasets and pipelines with **DVC**.
- **Wednesday:** Serve predictions via **FastAPI + Docker** with strict input validation.
- **Thursday:** Monitor live inputs/outputs and catch **Data Drift** and **Concept Drift**.
- **Friday:** Put all four pieces together in the **Worked Template Build** and demonstrate the live **Exit Gate**.

---

## 2. Local Laptop Setup (Windows, macOS, Linux)

### Windows (PowerShell)
```powershell
cd ml-course
powershell -File scripts/setup.ps1 -Local
pytest tests/ -v
```
*(Or use Docker Desktop: `powershell -File scripts/setup.ps1`.)*

### macOS / Linux / Git Bash
```bash
cd ml-course
bash scripts/setup.sh --local
pytest tests/ -v
```
*(Or use Docker Desktop: `bash scripts/setup.sh`.)*

Verify the API is live:
```bash
curl -s http://localhost:8000/health
```

---

## 3. Your Evening Rhythm (~2 Hours After Every Class)
1. **Tutor Agent (30 min):** Rebuild today's story in your own words using the day's Story Anchor.
2. **Practice Agent (45 min):** Complete hands-on tasks with saved evidence (files, terminal outputs).
3. **Coding Agent (30 min):** Build and review code using the hint ladder (`question -> hint -> outline -> code`).
4. **Quiz Agent (15 min):** Closed-book quiz on today only; log weak areas into your **Candidate State** (`.candidate/state.md`).
5. **Daily Report (5 min):** Send the Daily Report block to your instructor the same evening.

Full copy-paste prompts for every day are in [Candidate Prompts](../course/candidate-prompts.md).

---

## 4. Fraud API Quick Reference
Base URL: `http://localhost:8000`

| Method | Path | Purpose |
|---|---|---|
| `GET` | `/health` | Liveness + active model version |
| `GET` | `/v1/model-info` | Active parameters, metrics, feature list |
| `POST` | `/v1/predict` | Score a transaction (`200` JSON or `422` validation error) |
| `POST` | `/v1/rollback` | Restore baseline model / adjust threshold |
| `GET` | `/v1/monitor/drift` | Live PSI, KS p-value, p95 latency, alerts |
| `POST` | `/v1/monitor/simulate` | Simulate clean or drifted traffic |
| `GET` | `/metrics` | Prometheus metrics |

---

## 5. Weekend Self-Test & Handoff to Week 3
After Friday's demo & Weekly Rollup, take the closed-book self-test in [Weekend Follow-Up & Self-Test](../course/modules/06-weekend-followup-selftest.md). Week 3 shifts from tabular transactions to language—and everything you proved here returns in Weeks 4–5 as production AI engineering.
