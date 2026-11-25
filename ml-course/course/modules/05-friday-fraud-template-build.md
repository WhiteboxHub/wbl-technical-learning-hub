# Friday — Worked Template Build: MLOps Fraud Detection System

**Story anchor:** *The lab notebook, the time machine, the restaurant, and the lighthouse — one system. Friday is the retelling of the whole week's story, with the candidates holding the pen.*

---

## Run Sheet (AM + PM Sessions)
Build and verify the **Fraud Detection** template (`ml-course/`) end to end in class, checkpointing each stage against the guide:

1. **Stage 1 — Data & DVC Versioning (`fraud_system/data_gen.py`, `dvc.yaml`)**
   - Generate `data/transactions.csv`, track with DVC, verify `params.yaml` controls data version & split.
   - *Checkpoint:* Dataset hash and `prepare` stage reproducible via `dvc repro`.
2. **Stage 2 — Feature Handling & Logistic Regression (`fraud_system/features.py`, `fraud_system/train.py`)**
   - Shared feature engineering (`log_amount`, `amount_per_tx_24h`, `is_night`, `high_risk_intl`) + `StandardScaler` + balanced `LogisticRegression`.
   - *Checkpoint:* `train.py` produces `artifacts/model.joblib`, `metrics.json`, and `reference_stats.json`.
3. **Stage 3 — MLflow Tracking & Registry (`fraud_system/train.py`, `fraud_system/evaluate.py`)**
   - Log params, Precision/Recall/F1/ROC-AUC/PR-AUC, artifacts, Git/data lineage tags; register `fraud-detector` and promote through Staging -> Production.
   - *Checkpoint:* Two runs comparable in MLflow UI (`:5000`); model registered.
4. **Stage 4 — FastAPI + Docker + CI/CD (`fraud_system/serve.py`, `Dockerfile`, `.github/workflows/ci.yml`)**
   - Serve `/health`, `/v1/predict`, `/v1/model-info`, `/v1/rollback`, `/metrics`; verify `422` on invalid transactions; run `pytest tests/ -v`; build Docker image.
   - *Checkpoint:* Container answers `scripts/smoke.sh` / `scripts/smoke.ps1` with all checks green.
5. **Stage 5 — Monitoring & Live Drift Injection (`fraud_system/monitor.py`, `web/index.html`, `scripts/break.*`)**
   - Open `http://localhost:8000`, inject drift live (`scripts/break.sh data-drift` or UI button), observe PSI/KS alert trigger, then restore baseline (`scripts/fix.sh`).
   - *Checkpoint:* Monitoring view transitions `HEALTHY -> ALERT` on injected drift and returns cleanly on reset.

> **Overflow Rule:** Any stage not finished in class on Friday becomes candidate self-work over the weekend (no class); the instructor checks it in the weekend follow-up, and it is finished on Monday if needed.

---

## Final Demo & Exit Gate (Demonstrable Outcomes)
There are **no invented numeric pass thresholds**. Each candidate demonstrates four concrete outcomes live:
1. **Tracked MLflow experiment and a registered model** (params, metrics, artifacts, lineage).
2. **DVC-versioned dataset and reproducible pipeline** (`dvc repro` / byte-exact checkout).
3. **Model served from a Docker container behind FastAPI** (`/health`, valid `200` + invalid `422` `/v1/predict`).
4. **Monitoring view that detects injected drift** (`GET /v1/monitor/drift` or Console UI firing alert on live drift injection).

---

## Tutor Agent Prompt to Assign After Class
> Tutor Agent: This week was Worked Template Build - MLOps Fraud Detection System. Retell the week's story with me, day by day, one question at a time. Where my retelling breaks, reteach that piece only. End with the three things I must practise before next week.
