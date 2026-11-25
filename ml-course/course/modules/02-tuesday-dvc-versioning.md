# Tuesday — DVC + Data and Pipeline Versioning

**Story anchor:** *The time machine for data: Git remembers the code, DVC remembers the world the code ran on.*
Open with it, return to it at every topic change, and close with it. Time: ~3 hours.

---

## 1. Topics to Cover Today
1. Why Git alone cannot version data
2. DVC remotes, `.dvc` files, `checkout` and `pull`
3. Pipelines as code: stages, dependencies, `dvc repro`
4. Data versioning discipline: what changes, what must never change silently
5. MLflow + DVC together: the full lineage picture

## 2. The Class — Intro, Topics, Conclusion
- **Intro (first 15 min):** Hook with the time-machine anchor. Destination in one sentence: *By tonight, you can roll any dataset back byte-for-byte and re-run an entire multi-stage ML pipeline with one command.* Show `tue_01_dvc_version_rollback.py` finishing with `byte_match_v1=True`. Three questions: (1) Why does Git choke on data? (2) How does `dvc repro` save time and prevent stale artifacts? (3) How do DVC and MLflow split responsibility?
- **Topics (~2h30m with break, demo-first):**
  1. Silent edit traced with hashes (`tue_03_silent_edit_lineage.py`).
  2. DVC dataset versioning & byte-for-byte rollback (`tue_01_dvc_version_rollback.py`).
  3. Two-stage pipeline reproduced incrementally (`tue_02_dvc_pipeline_repro.py` + inspecting [dvc.yaml](../../dvc.yaml)).
- **Conclusion (last 15 min):** Retell the time-machine story in 1 minute. Three things that survive the night: (1) Git tracks code + `.dvc` pointers, DVC tracks large data; (2) `dvc repro` runs only dirty stages; (3) Git + DVC + MLflow = full lineage. Run Exit Check out loud. Tomorrow's hook: *"Our lab notebook and time machine are rock solid—tomorrow the restaurant opens and real users hit our model over HTTP."*

## 3. What the Candidate Must Know
- Initialise DVC on a project and version a dataset
- Define a pipeline and reproduce it with one command
- Roll a dataset back to a previous version and prove it

## 4. Slides (`MLops` 222-page PDF)
- Partial mentions only: **Slides 30, 56–57, 102, 105, 218–219**.
- *Note:* No dedicated website slides for DVC commands/pipelines — teach directly from **5A** and **5D** demos.

---

## 5A. Topic Material (Teachable Out Loud)
1. **Why Git Alone Cannot Version Data:** Git stores diffs of small text files in `.git/objects` forever; committing 500 MB CSVs or images bloats every clone and still gives no pipeline DAG. *Worked example:* A 200 MB dataset updated 10 times makes a 2 GB `.git` folder. *Misconception:* "Git LFS solves pipelines too" (LFS stores blobs, not `dvc.yaml` stage dependencies). *5-min exercise:* Compare `transactions.csv` size vs a 100-byte `.dvc` MD5 pointer file.
2. **DVC Remotes, `.dvc` Files, `checkout` & `pull`:** `dvc add data/transactions.csv` creates `transactions.csv.dvc` (small YAML with MD5 hash) and puts `transactions.csv` in `.gitignore`. `dvc push` sends data to a remote (local folder, S3); `git checkout <tag> && dvc checkout` (or `dvc pull`) restores the exact historical bytes. *Worked example:* `tue_01_dvc_version_rollback.py`. *Misconception:* "Committing `.dvc` pushes the CSV to GitHub" (it only pushes the pointer!). *5-min exercise:* Inspect a `.dvc` file and explain its `md5` and `size` fields.
3. **Pipelines as Code (`dvc.yaml`, `dvc repro`):** Declare stages (`prepare -> train -> evaluate`), `deps`, `params`, `outs`. `dvc repro` hashes every input and skips unchanged stages. *Worked example:* `tue_02_dvc_pipeline_repro.py` changes `C` in `params.yaml` and skips `prepare`. *Misconception:* "Pipelines must rerun from scratch every time." *5-min exercise:* Read [dvc.yaml](../../dvc.yaml) and predict which stages rerun if `model.threshold` changes.
4. **Data Versioning Discipline:** Raw data should be immutable/append-only; cleaning scripts belong in versioned code, never manual Excel edits. *Worked example:* `tue_03_silent_edit_lineage.py`. *Misconception:* "Fixing one typo in `transactions.csv` doesn't need a new version." *5-min exercise:* Name 2 things that must never change silently in fraud training data.
5. **MLflow + DVC Together (Full Lineage):** Git commits the code + `dvc.lock`; DVC owns data snapshots & pipeline DAG; MLflow logs the resulting metrics, `data_sha256`, `git_sha`, and model artifacts. *Worked example:* `fraud_system/train.py` logging `data_sha256` alongside MLflow metrics. *Misconception:* "Pick either DVC or MLflow" (they are complementary). *5-min exercise:* Trace a Production model back to its exact CSV snapshot using MLflow -> Git -> DVC.

## 5B. Explanation Instructor Guide
- **Topic 1/2 — Say first:** *"Git is great at remembering 500 lines of Python, terrible at remembering 5 GB of transactions."* **Metaphor:** Library card catalog (`.dvc` file in Git) vs the heavy book in the warehouse (DVC remote). **Ask:** *"If I run `git push` after `dvc add`, did my dataset reach GitHub?"* **Wrong answer:** *"Yes."* **Correction:** *"Only the 4-line receipt (`.dvc`) went to GitHub; `dvc push` moves the actual data."*
- **Topic 3 — Say first:** *"Watch `dvc repro` skip work it already proved."* **Ask:** *"If I tune `C=2.5`, should data preparation run again?"* **Wrong answer:** *"Yes, to be safe."* **Correction:** *"No—`prepare`'s inputs didn't change, so DVC reuses the exact cached output."*
- **Two places candidates get lost:**
  1. *Forgetting `git checkout` + `dvc checkout` are a two-step pair:* Remind them: *"Git switches the receipt; DVC fetches the box."*
  2. *Editing `dvc.lock` by hand:* Never edit `dvc.lock`; always run `dvc repro`.

## 5C. Local Setup (Windows / Mac / Linux)
1. **Verify tools:** `git --version`, `dvc --version` (installed via `requirements.txt` in `.venv` or inside Docker container).
2. **Commands in order:**
   - `python -m fraud_system.data_gen --version v1 --out data/transactions.csv`
   - `python demos/tue_01_dvc_version_rollback.py`
3. **Top 3 Setup Failures:**
   - *`dvc: command not found`:* `.venv` not activated -> activate `.venv` or prefix with `python -m dvc`.
   - *`not a git repository` error:* Running `dvc init` outside a Git repo -> always `git init` first (demos use isolated temp repos).
   - *Windows symlink/cache permissions:* DVC defaults to copy/hardlink cleanly on Windows when not using symlinks; avoid Admin-only symlink configs.

## 5D. Demo Programs (`demos/`)
- **Demo 1 (Version & Rollback):** `python demos/tue_01_dvc_version_rollback.py` -> Live variation: `--rows-v2 3500`
- **Demo 2 (Incremental `dvc repro`):** `python demos/tue_02_dvc_pipeline_repro.py` -> Live variation: `--change-stage prepare` vs `--change-stage none`
- **Demo 3 (Silent-Edit Mystery):** `python demos/tue_03_silent_edit_lineage.py` -> Live variation: `--no-edit`

## 6. Real Scenarios
- Compliance investigation asking: *"What exact data trained the fraud model live in March?"*
- A data supplier quietly backfilling/fixing history and breaking downstream models.
- Multi-team ML projects where datasets evolve weekly.

## 7. Exit Check (With Answers)
1. **Q:** Why not just put the CSV in Git?
   **A:** Git is built for small text; large binary data bloats it and still gives no pipeline or remote discipline.
2. **Q:** What does `dvc repro` guarantee?
   **A:** Only stages whose inputs changed are rerun — the pipeline is reproducible and incremental.
3. **Q:** MLflow and DVC — who owns what?
   **A:** DVC versions data and pipelines; MLflow tracks experiments and the model registry. Together they give full lineage.

## Tutor Agent Prompt to Assign After Class
> Tutor Agent: Today we covered DVC + Data and Pipeline Versioning. Teach it back to me using the story anchor (The time machine for data: Git remembers the code, DVC remembers the world the code ran on). Ask me one question at a time, wait for my answer, and correct me before moving on. Do not do my assignment. End by naming my two weakest points today.
