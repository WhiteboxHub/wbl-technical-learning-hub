# Instructor steps: how to start and take the class

Course: **Week 2 PM — Production ML & MLOps** (MLflow, DVC, FastAPI + Docker, Monitoring + Drift Detection, and Worked Fraud Detection Template Build), taught with an AI co-pilot and a shared Fraud Detection MLOps stack.
Project folder: `ml-course/` (inside this repo). More detail: `ml-course/docs/instructor-guide.md` and `ml-course/docs/class-day-quickstart.md`.

## Before class

1. **Open the right folder.** Open `ml-course/` in a **new AI session** so `.claude/skills/` load at session start (`setup-ml-class`, `teach-ml-class`).
2. **Start Docker Desktop** (or prepare `.venv` with `scripts/setup.ps1 -Local` / `scripts/setup.sh --local`).
3. **Open your slides:** `MLops` (Course Material > Presentations, 222-page deck). Note the Tuesday DVC slide gap — teach Tuesday directly from `course/modules/02-tuesday-dvc-versioning.md` sections `5A` and `5D`.

## Starting the class

1. Say **"set up the class"** (runs `scripts/setup.sh` or `scripts/setup.ps1`, starts MLflow `:5000` + Fraud API `:8000`, runs `scripts/smoke.*`, and prints **READY**).
2. Say **"teach monday"** (or `tuesday`, `wednesday`, `thursday`, `friday`).
3. Confirm whether your screen is shared with candidates. If yes, Exit Check and Beat answers stay hidden until you type `answer`.

## Start commands by day

| Day | Session & Story Anchor | Key Commands / URLs |
|---|---|---|
| **Monday** | ML Lifecycle + MLflow (*The lab notebook*) | `python demos/mon_01_unreproducible.py`, `mon_02_mlflow_tracking.py`, `mon_03_registry_promotion.py` · MLflow UI `http://localhost:5000` |
| **Tuesday** | DVC + Data & Pipeline Versioning (*The time machine for data*) | `python demos/tue_01_dvc_version_rollback.py`, `tue_02_dvc_pipeline_repro.py`, `tue_03_silent_edit_lineage.py` |
| **Wednesday** | Model Deployment — FastAPI + Docker (*The restaurant opens*) | `python demos/wed_01_fastapi_service.py`, `wed_02_docker_predict.py`, `wed_03_validation_vs_corrupt.py` · Swagger `http://localhost:8000/docs` |
| **Thursday** | Monitoring + Drift Detection (*The lighthouse keeper*) | `python demos/thu_01_drift_stream.py`, `thu_02_monitoring_readout.py`, `thu_03_alert_tuning.py` · Console `http://localhost:8000` |
| **Friday** | Worked Template Build — Fraud Detection (*All 4 anchors*) | `dvc repro` · `pytest tests/ -v` · `scripts/break.ps1 data-drift` (or `break.sh`) · `scripts/fix.ps1` (or `fix.sh`) |
| **Weekend** | No class — Instructor follow-up only | Review Daily Reports + Friday Weekly Rollup; see `course/modules/06-weekend-followup-selftest.md` |

## During class

The co-pilot walks one beat at a time (Story Anchor -> demo-first -> explanation -> question).

| You say | What happens |
|---|---|
| `next` / `back` | Move between beats |
| `repeat` | Re-run the current demo |
| `skip` | Skip beat and log it |
| `answer` | Reveal the held answer |
| `break <fault>` | Inject live fault (`data-drift`, `concept-drift`, `bad-schema`, `latency-spike`) |
| `fix` | Clear faults and reset monitoring window (`scripts/fix.*`) |
| `end` | Run 1-minute retelling, 3 takeaways, Exit Check, tomorrow's hook & Tutor prompt |

## If something goes wrong

| Problem | Do this |
|---|---|
| Port `5000` busy on macOS | Disable **AirPlay Receiver** in System Settings, or map `5001:5000` in `docker-compose.yml` |
| Windows `python3` opens Microsoft Store | Use `python` or `.venv\Scripts\python.exe` |
| Old drift alerts remain on screen | Run `scripts/fix.sh` or `powershell -File scripts/fix.ps1` |
| Stack needs a clean restart | `scripts/setup.sh --stop` then `scripts/setup.sh` (or `scripts/setup.ps1 -Stop` then `scripts/setup.ps1`) |

## Candidates

Send candidates `ml-course/docs/student-guide.md` and `ml-course/course/candidate-prompts.md`. All tasks run locally on their laptop.
