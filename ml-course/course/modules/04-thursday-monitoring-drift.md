# Thursday — Monitoring + Drift Detection

**Story anchor:** *The lighthouse keeper: the model does not announce when the world has moved on.*
Open with it, return to it at every topic change, and close with it. Time: ~3 hours.

---

## 1. Topics to Cover Today
1. What to monitor: inputs, outputs, performance, latency, errors
2. Data drift vs concept drift — the world changes vs the meaning changes
3. Drift signals and statistics in plain terms
4. Alerting without alarm fatigue
5. Retraining triggers and the decision to retire a model

## 2. The Class — Intro, Topics, Conclusion
- **Intro (first 15 min):** Hook with the lighthouse keeper anchor. Destination in one sentence: *By tonight, your deployed Fraud API watches its own inputs, outputs, and latency, and raises clean alerts when the world shifts.* Show `http://localhost:8000` flipping from `HEALTHY` to `ALERT` after drift injection. Three questions: (1) What are the 4 pillars of ML monitoring? (2) How do data drift and concept drift differ? (3) How do we avoid alert fatigue?
- **Topics (~2h30m with break, demo-first):**
  1. Synthetic drift plotted/printed live until alarm fires (`thu_01_drift_stream.py`).
  2. Monitoring readout & concept drift (`thu_02_monitoring_readout.py`, slang-dictionary / fraud-tactic analogy).
  3. Alert storm tuned down to 3 actionable alerts (`thu_03_alert_tuning.py`).
- **Conclusion (last 15 min):** Retell the lighthouse story in 1 minute. Three things that survive the night: (1) Deployment is day 1, not the finish line; (2) Data drift = input shift, Concept drift = rule shift; (3) Alert only on actionable signals. Run Exit Check out loud. Tomorrow's hook: *"Tomorrow you hold the pen—we assemble the full Fraud Detection system from raw data to live drift alarm."*

## 3. What the Candidate Must Know
- Instrument a deployed model with input and output monitoring
- Distinguish data drift from concept drift with examples
- Define a retraining trigger you could defend in a review

## 4. Slides (`MLops` 222-page PDF)
- Monitoring, Prometheus + Grafana, CloudWatch: **Slides 173–183**
- Data Drift vs Concept Drift, Evidently AI, Alibi-Detect: **Slides 184–191**
- Alerting, Logging, Closed Feedback Loop, Retraining & Rollback: **Slides 192–221**
- *Note:* Attached `MLops` PDF has full coverage (`173–221`) even where the website outline had partial slides.

---

## 5A. Topic Material (Teachable Out Loud)
1. **What to Monitor (Inputs, Outputs, Performance, Latency, Errors):** A model rarely crashes with an HTTP 500 when it rots—it returns HTTP `200` with wrong answers. Monitor 4 layers: Data Inputs (missing/OOD/distribution), Model Outputs (predicted fraud rate, confidence), Infra (`p50`/`p95` latency, error rate), and Ground-Truth Performance (when delayed labels arrive). *Worked example:* `GET /v1/monitor/drift` and `GET /metrics`. *Misconception:* "HTTP 200 OK means the ML model is healthy." *5-min exercise:* Hit `/v1/monitor/drift` and read all 4 telemetry dimensions.
2. **Data Drift vs Concept Drift:**
   - **Data drift:** `P(X)` changes (e.g., holiday spending spikes, higher international volume), while what counts as fraud stays the same.
   - **Concept drift:** `P(Y|X)` changes (inputs look normal, but fraudsters switch to small daytime card-present micro-transactions—like a slang dictionary expiring).
   *Worked example:* `thu_02_monitoring_readout.py --concept-drift`. *Misconception:* "Input drift checks catch everything" (concept drift hides behind stable inputs!). *5-min exercise:* Classify 3 real shifts into Data vs Concept drift.
3. **Drift Signals & Statistics in Plain Terms:** Compare live feature window against training baseline (`artifacts/reference_stats.json`) using **PSI** (Population Stability Index: `<0.1` stable, `0.15–0.25` warn, `>=0.25` alert) and **KS test** (two-sample Kolmogorov-Smirnov p-value). *Worked example:* `compute_psi` in `fraud_system/monitor.py`. *Misconception:* "Compare averages only" (two very different distributions can share the exact same mean). *5-min exercise:* Run `thu_01_drift_stream.py --psi-alert 0.50` and watch when the alarm fires.
4. **Alerting Without Alarm Fatigue:** 50 Slack alerts/day train engineers to mute the channel. Every alert must map to an owner and an action. *Worked example:* `thu_03_alert_tuning.py --mode noisy` vs `--mode tuned`. *Misconception:* "Alert on every feature shift immediately." *5-min exercise:* Convert 5 noisy raw metrics into 2 actionable alerts.
5. **Retraining Triggers & Model Retirement:** Three defensible triggers: **Scheduled** (every 7/30 days), **Metric-based** (`recall < 0.70` or `p95 > 200ms`), **Data-based** (`PSI >= 0.25`). Always gate retrained models (`new_f1 >= prod_f1`) before promoting; retire models when problem/schema changes permanently. *Worked example:* `fraud_system/evaluate.py`. *Misconception:* "Auto-deploy every retrained model blindly." *5-min exercise:* Write a 1-sentence retraining trigger policy for Fraud Detection.

## 5B. Explanation Instructor Guide
- **Topic 1 — Say first:** *"A web server yells 500 when it breaks. An ML model smiles, returns 200 OK, and loses the bank money."* **Metaphor:** Lighthouse keeper watching fog roll in. **Ask:** *"If our API has 0% HTTP errors and 5ms latency, can the model still be failing?"* **Wrong answer:** *"No, zero errors means it works."* **Correction:** *"That only proves the plumbing works, not the predictions."*
- **Topic 2 — Say first:** *"Imagine a slang dictionary from 2015—same words, completely different meanings."* **Ask:** *"Customer ages shift older -> Data or Concept drift? Attackers invent a new fraud trick with normal-looking amounts -> Data or Concept drift?"* **Wrong answer:** *"Both are data drift."* **Correction:** *"Population shift = Data drift; meaning/rule shift = Concept drift."*
- **Two places candidates get lost:**
  1. *KS p-value interpretation:* Small p-value (`< 0.01`) = distributions are **different** (drift!).
  2. *Why labels lag in production:* Fraud chargebacks arrive days/weeks later, so input/output drift is our **early warning** before Recall drops.

## 5C. Local Setup (Windows / Mac / Linux)
1. **Verify dependencies:** `python -c "import scipy, fastapi; print('OK')"` (plus optional Prometheus `docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d`).
2. **Run:** `python demos/thu_01_drift_stream.py`
3. **Top 3 Setup Failures:**
   - *`artifacts/reference_stats.json` missing:* Run `python -m fraud_system.train` once.
   - *Previous drift batch still in window:* Call `scripts/fix.sh` (or `POST /v1/monitor/reset`).
   - *`scipy` missing:* Install `requirements.txt` inside `.venv`.

## 5D. Demo Programs (`demos/`)
- **Demo 1 (Drift Stream):** `python demos/thu_01_drift_stream.py` -> Live variation: `--psi-alert 0.50`
- **Demo 2 (Monitoring Readout):** `python demos/thu_02_monitoring_readout.py` -> Live variation: `--concept-drift`
- **Demo 3 (Alert Tuning):** `python demos/thu_03_alert_tuning.py` -> Live variation: `--mode tuned`

## 6. Real Scenarios
- A fraud model decaying as attackers change behaviour.
- A demand model broken by a pandemic-shaped shift in buying.
- A hiring model whose applicant population shifted over two years.

## 7. Exit Check (With Answers)
1. **Q:** Data drift vs concept drift?
   **A:** Data drift: the input distribution changes. Concept drift: the relationship between inputs and the right answer changes.
2. **Q:** Performance drops but inputs look stable. Likely cause?
   **A:** Concept drift — the world's rules changed, not the data's shape.
3. **Q:** Why not alert on everything?
   **A:** Alarm fatigue: a team that gets fifty alerts a day reads none of them.

## Tutor Agent Prompt to Assign After Class
> Tutor Agent: Today we covered Monitoring + Drift Detection. Teach it back to me using the story anchor (The lighthouse keeper: the model does not announce when the world has moved on). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.
