# Wednesday — Model Deployment: FastAPI + Docker

**Story anchor:** *The restaurant opens: the recipe leaves the test kitchen and has to survive paying customers.*
Open with it, return to it at every topic change, and close with it. Time: ~3 hours.

---

## 1. Topics to Cover Today
1. Serving patterns: REST API, batch, streaming — and choosing
2. FastAPI model service: schema, validation, error behaviour
3. Containerising the service with Week 1's Docker skills
4. Health checks, versioning the endpoint, rollback thinking
5. Latency, throughput, and the cost of a slow prediction

## 2. The Class — Intro, Topics, Conclusion
- **Intro (first 15 min):** Hook with the restaurant anchor. Destination in one sentence: *By tonight, your baseline Fraud model leaves the notebook and serves validated real-time predictions from a Docker container.* Show `http://localhost:8000/docs` and a live `curl` prediction first. Three questions: (1) When do you choose REST vs batch vs streaming? (2) Why must an API validate inputs strictly? (3) How do Docker + versioned endpoints make rollback instant?
- **Topics (~2h30m with break, demo-first):**
  1. Earlier baseline Fraud model wrapped in FastAPI (`wed_01_fastapi_service.py` + `fraud_system/serve.py`).
  2. Container built & run; predictions served live (`wed_02_docker_predict.py` + `http://localhost:8000`).
  3. Bad request sent deliberately (`amount=-50, hour_of_day=27`) -> watch Pydantic validation block corruption (`wed_03_validation_vs_corrupt.py`).
- **Conclusion (last 15 min):** Retell the restaurant story in 1 minute. Three things that survive the night: (1) Validation prevents silent garbage predictions; (2) Containers carry the exact runtime environment; (3) Always design `/health`, `/v1/` versioning, and rollback before launch. Run Exit Check out loud. Tomorrow's hook: *"The restaurant is open and serving customers—but how do we notice when our ingredients spoil or customers' tastes change?"*

## 3. What the Candidate Must Know
- Serve a trained model behind a FastAPI endpoint with input validation
- Containerise the service and run it from the image
- Explain how this deployment would roll back

## 4. Slides (`MLops` 222-page PDF)
- Deployment & Serving Patterns (Online vs Batch): **Slides 150–153**
- Self-Hosted FastAPI + Docker + MLflow Serve: **Slides 154–160**
- Cloud Deployment, CI/CD & Rollback/Ops Best Practices: **Slides 161–172**, **217**

---

## 5A. Topic Material (Teachable Out Loud)
1. **Serving Patterns (REST vs Batch vs Streaming):** Online REST API (`<100ms`, fraud check at checkout), Batch (nightly churn/credit scoring), Streaming (Kafka event scoring). *Worked example:* Checkout card swipe cannot wait for tonight's batch job—needs `/v1/predict` now. *Misconception:* "Everything should be a REST API" (nightly reporting is cheaper as batch). *5-min exercise:* Match 3 business cases (checkout fraud, monthly credit score, clickstream anomaly) to serving patterns.
2. **FastAPI Model Service (Schema, Validation, Errors):** Pydantic `TransactionIn` enforces types and ranges (`amount > 0`, `0 <= hour_of_day <= 23`). Shared `engineer_features()` guarantees training-serving parity. *Worked example:* `wed_03_validation_vs_corrupt.py` returns HTTP `422` instead of silently scoring `-50` dollars. *Misconception:* "Sklearn throws an error on bad domain values" (sklearn happily computes math on `hour_of_day=99`!). *5-min exercise:* Hit `/docs` and send a negative amount.
3. **Containerising with Docker:** `Dockerfile` packages Python 3.11, `requirements.txt`, `fraud_system/`, and `uvicorn` so staging == production. *Worked example:* `docker compose up --build -d` + `wed_02_docker_predict.py`. *Misconception:* "It works on my laptop so it'll work on ECS." *5-min exercise:* Inspect [Dockerfile](../../Dockerfile) and identify why `requirements.txt` is copied before source code (layer cache).
4. **Health Checks, Endpoint Versioning, Rollback Thinking:** `/health` lets load balancers know the model is loaded; `/v1/predict` lets clients migrate safely; `/v1/rollback` (or reverting Docker image tag / MLflow `@champion` alias) recovers within seconds. *Worked example:* `POST /v1/rollback` in `fraud_system/serve.py`. *Misconception:* "Rollback means retraining." *5-min exercise:* Describe how to roll back a bad Fraud threshold in under 30 seconds.
5. **Latency, Throughput & Cost of Slow Predictions:** Load model **once at startup** (`lifespan`), never inside `/predict`. Track `p50`/`p95` latency (`latency_ms` in response). *Worked example:* `scripts/break.sh latency-spike` simulates a `250ms` bottleneck. *Misconception:* "Average latency tells the whole story" (p95/p99 shows what worst-case users feel). *5-min exercise:* Call `/v1/predict` twice and compare `latency_ms`.

## 5B. Explanation Instructor Guide
- **Topic 1 — Say first:** *"Today the recipe leaves the test kitchen—paying customers are at the tables."* **Metaphor:** Test kitchen vs live restaurant service. **Ask:** *"A card is swiped at a terminal right now. Batch job or REST API?"* **Wrong answer:** *"Batch every hour."* **Correction:** *"By midnight the thief is gone; checkout fraud requires real-time REST."*
- **Topic 2 — Say first:** *"Watch what happens if we pass negative dollars to an unvalidated model vs FastAPI."* **Ask:** *"Why didn't scikit-learn complain about `hour_of_day = 27`?"* **Wrong answer:** *"Because 27 is valid."* **Correction:** *"Because to a matrix multiplication, 27 is just a float; Pydantic is our bouncer at the door."*
- **Two places candidates get lost:**
  1. *Loading `model.joblib` per request vs at startup:* Show `lifespan` in `serve.py`.
  2. *Training-serving feature skew:* Point out `fraud_system/features.py` is imported by both `train.py` and `serve.py`.

## 5C. Local Setup (Windows / Mac / Linux)
1. **Verify Docker & Python:** `docker --version`, `docker compose version`, `uvicorn --version`.
2. **Commands in order:**
   - `docker compose up --build -d`
   - `bash scripts/smoke.sh` (or `powershell -File scripts/smoke.ps1`)
3. **Top 3 Setup Failures:**
   - *Port 8000 already in use:* Prior `uvicorn` or `http-course` container running -> stop old container (`docker compose down` in `http-course`).
   - *Docker Desktop not running (exit 11):* Start Docker Desktop and wait for engine green icon.
   - *`model.joblib` missing when running locally:* Run `python -m fraud_system.train` first (or `serve.py` auto-trains on startup).

## 5D. Demo Programs (`demos/`)
- **Demo 1 (FastAPI Service):** `python demos/wed_01_fastapi_service.py` -> Live variation: `--amount 4500 --risk 0.92`
- **Demo 2 (Docker Container Predict):** `python demos/wed_02_docker_predict.py` -> Live variation: `--amount 25.0`
- **Demo 3 (Validation vs Corrupt):** `python demos/wed_03_validation_vs_corrupt.py` -> Live variation: `--amount 120`

## 6. Real Scenarios
- A pricing model serving a web storefront in real time.
- A document classifier behind an internal API.
- Any Week 1 Docker deployment, now with an ML model inside.

## 7. Exit Check (With Answers)
1. **Q:** Why validate inputs at the API?
   **A:** Models fail silently on malformed input; validation turns silent corruption into a visible error.
2. **Q:** Why containerise the model service?
   **A:** The environment travels with the model — it runs the same in staging and production.
3. **Q:** Sync API or batch?
   **A:** Sync when a user waits for one answer; batch when many predictions can be computed on a schedule.

## Tutor Agent Prompt to Assign After Class
> Tutor Agent: Today we covered Model Deployment - FastAPI + Docker. Teach it back to me using the story anchor (The restaurant opens: the recipe leaves the test kitchen and has to survive paying customers). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.
