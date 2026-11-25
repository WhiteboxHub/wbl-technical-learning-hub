# Monday — ML Lifecycle + MLflow Experiment Tracking

**Story anchor:** *The lab notebook: a scientist who cannot reproduce last Tuesday's result has an anecdote, not a result.*
Open with it, return to it at every topic change, and close with it (promise -> telling -> retelling). Time: ~3 hours.

---

## 1. Topics to Cover Today
1. The ML lifecycle end to end: data, train, evaluate, register, deploy, monitor
2. Why experiments without tracking become archaeology
3. MLflow tracking: params, metrics, artifacts, runs
4. The model registry: stages, versions, lineage
5. What "reproducible" actually requires: code + data + params + environment

## 2. The Class — Intro, Topics, Conclusion
- **Intro (first 15 min):** Hook with the lab notebook anchor. Destination in one sentence: *By tonight, every Fraud model run you train is logged, comparable, and promotable with full lineage.* Show the finished MLflow UI (`http://localhost:5000`) and `mon_02_mlflow_tracking.py` output first. Name three questions we will answer: (1) Why does untracked ML break on rerun? (2) What goes into an MLflow run? (3) How does a winning model earn a promotion?
- **Topics (~2h30m with break, demo-first):**
  1. Untracked experiment rerun live (`mon_01_unreproducible.py`) -> result refuses to match.
  2. MLflow UI explored: two Fraud runs compared side by side (`mon_02_mlflow_tracking.py`).
  3. Model Registry staging walked through as promotion through ranks (`mon_03_registry_promotion.py`).
- **Conclusion (last 15 min):** Retell the lab-notebook story in 1 minute. Three things that survive the night: (1) Untracked runs are anecdotes; (2) MLflow logs params, metrics, artifacts & lineage; (3) Reproducibility needs code + data + params + environment. Run Exit Check out loud. Tomorrow's hook: *"MLflow remembers your code and parameters—but what happens if someone silently edits the CSV under your feet?"*

## 3. What the Candidate Must Know
- Log an experiment in MLflow with params, metrics, and artifacts
- Find and compare two runs and say what changed the result
- Register a model version with its lineage intact

## 4. Slides (`MLops` 222-page PDF)
- Lifecycle & Why MLOps: **Slides 1–22**
- Trackable & Reproducible Training: **Slides 58–71**, **102–106**
- MLflow Tracking, UI & Registry: **Slides 77–88**, **116–118**, **146–149**
- Fraud Detection Metric Motivation: **Slides 120**, **126–127**, **140**

---

## 5A. Topic Material (Teachable Out Loud)
1. **End-to-End ML Lifecycle:** Building the model is 10% of the work; 90% is Data -> Train -> Evaluate -> Register -> Deploy -> Monitor -> Retrain. *Worked example:* A Fraud Logistic Regression model trained on 2,000 transactions isn't done until it's registered, served behind FastAPI, and watched for drift. *Misconception:* "99% accuracy means ready for prod" (at 0.2% fraud, predicting all-legit gives 99.8% accuracy and catches zero fraud—use Recall/Precision/F1). *5-min exercise:* Sketch the 6 lifecycle stages for a credit-card fraud filter and pick the primary metric.
2. **Why Untracked Experiments Become Archaeology:** Changing `C`, `threshold`, or split seeds in a notebook overwrites memory. *Worked example:* Running `mon_01_unreproducible.py` twice yields different Recall/F1. *Misconception:* "I'll remember what parameters gave 0.85 F1." *5-min exercise:* Change one value in `mon_01_unreproducible.py` and notice no record remains of the prior run.
3. **MLflow Tracking (`params`, `metrics`, `artifacts`, `runs`):** A `run` is one page in the lab notebook: inputs (`log_param`), scores (`log_metric`), outputs (`log_artifact` / `log_model`). *Worked example:* `fraud_system/train.py` compares `C=0.1` vs `C=2.0` at `threshold=0.35`. *Misconception:* "MLflow replaces Git" (no—MLflow records the `git_sha` tag pointing to Git). *5-min exercise:* Run `mon_02_mlflow_tracking.py --threshold 0.25` and compare in MLflow UI.
4. **Model Registry (Stages, Versions, Lineage):** A folder of `model_v2_final_REAL.pkl` files has no lineage. Registry assigns monotonic versions (`v1`, `v2`), stage/alias transitions (`Staging` / `@challenger` -> `Production` / `@champion` -> `Archived`), and links back to the exact `run_id`. *Worked example:* `mon_03_registry_promotion.py`. *Misconception:* "Registry automatically re-trains models" (it governs approved model versions). *5-min exercise:* Inspect the registered `fraud-detector` version in MLflow UI and trace its `run_id`.
5. **Reproducibility = Code + Data + Params + Environment:** Missing any one of the four breaks reruns. *Worked example:* `mlruns/` stores `MLmodel`, `conda.yaml` / `requirements.txt`, `params.json`, `metrics.json`, plus `git_sha` and `data_sha256` tags. *Misconception:* "Setting `random_state=42` is enough." *5-min exercise:* List which of the 4 pillars `fraud_system/train.py` logs today and which one Tuesday (DVC) will strengthen.

## 5B. Explanation Instructor Guide
- **Topic 1 — Say first:** *"If I hand you a baked cake and lose the recipe, you can eat it once, not run a bakery."* **Metaphor:** Lab notebook vs scratched sticky notes. **Ask:** *"If fraud is 1% of transactions and my model says 'not fraud' for everything, what is its accuracy?"* **Wrong answer to expect:** *"1% or terrible!"* **Correction:** *"Actually 99%—which is why Accuracy lies on imbalanced fraud data."*
- **Topic 2/3 — Say first:** *"Watch these two runs of the exact same script."* **Ask:** *"Why did Tuesday's score vanish?"* **Wrong answer:** *"Because Python is broken."* **Correction:** *"Because nothing wrote down the seed, data slice, or `C` value."*
- **Topic 4/5 — Say first:** *"Raise your hand if you have a folder with `model_final2_v3.pkl`."* **Ask:** *"What does a Registry give us that Dropbox doesn't?"* **Wrong answer:** *"Faster training."* **Correction:** *"Lineage and safe promotion gates."*
- **Two places candidates get lost:**
  1. *Confusing parameters vs metrics:* Anchor with **"knobs you turn before training = params; grades you get after = metrics."**
  2. *Confusing MLflow Tracking vs Registry:* Anchor with **"Tracking is every messy draft in the notebook; Registry is the signed trophy shelf."**

## 5C. Local Setup (Windows / Mac / Linux)
1. **Python 3.10+ & Git:** `python --version` (`C:\Program Files\Python311\python.exe` on Windows if `python3` triggers Store) and `git --version`.
2. **Install & Verify:**
   - Windows: `powershell -File scripts/setup.ps1 -Local` -> verify `python -c "import mlflow, sklearn; print('OK')"`
   - Mac/Linux: `bash scripts/setup.sh --local` -> verify `python3 -c "import mlflow, sklearn; print('OK')"`
   - Docker option: `docker compose up --build -d` -> verify `curl -sf http://localhost:5000/health`
3. **Top 3 Setup Failures:**
   - *Port 5000 in use on macOS:* AirPlay Receiver uses `:5000` -> disable AirPlay Receiver or run `mlflow ui --port 5001`.
   - *Windows `python3` alias opens Microsoft Store:* Use `python` or `py -3`.
   - *Tracking URI mismatch:* Ensure `MLFLOW_TRACKING_URI=http://localhost:5000` (or default `./mlruns`) matches the running UI.

## 5D. Demo Programs (`demos/`)
- **Demo 1 (Unreproducible):** `python demos/mon_01_unreproducible.py` -> Live variation: `--fix-seed 42`
- **Demo 2 (MLflow Tracking):** `python demos/mon_02_mlflow_tracking.py` -> Live variation: `--threshold 0.20`
- **Demo 3 (Registry Promotion):** `python demos/mon_03_registry_promotion.py` -> Live variation: `--stage Staging`

## 6. Real Scenarios
- A team that lost its best model because nobody recorded its parameters.
- Regulated finance/healthcare audits requiring exact model lineage.
- Any team larger than one person touching the same model.

## 7. Exit Check (With Answers)
1. **Q:** A run scored best but nobody can rebuild it. What was missing?
   **A:** Tracking: params, code version, data version, and environment were not logged together.
2. **Q:** What does the registry add over a folder of model files?
   **A:** Versioning, stage transitions, and lineage — which model, from which run and data, is in production.
3. **Q:** Name the four things reproducibility needs.
   **A:** Code, data, parameters, and environment — all versioned together.

## Tutor Agent Prompt to Assign After Class
> Tutor Agent: Today we covered ML Lifecycle + MLflow Experiment Tracking. Teach it back to me using the story anchor (The lab notebook: a scientist who cannot reproduce last Tuesday's result has an anecdote, not a result). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.
