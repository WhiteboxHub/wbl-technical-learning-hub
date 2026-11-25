# Production ML & MLOps — Week 2 PM Course

Running example: **Fraud Detection System** — built step by step from an untracked experiment (Monday) to a DVC-versioned, MLflow-tracked, Dockerized FastAPI service with live PSI/KS drift detection (Friday template build).

## Guides & Curriculum
- [Course Table of Contents](docs/course-toc.md) — Week 2 PM syllabus & slide mapping to the 222-page `MLops` deck
- [Class-Day Quick Start](docs/class-day-quickstart.md) — 5-minute instructor checklist
- [Instructor Guide](docs/instructor-guide.md) — Mon–Fri cadence, story anchors, `5A–5D` prompts, troubleshooting
- [Student Guide](docs/student-guide.md) — Local setup (Win/Mac/Linux), Evening Rhythm, Fraud API reference, Self-Test
- [Candidate Prompts](course/candidate-prompts.md) — Copy-paste Tutor, Practice, Coding, Quiz & Daily Report prompts

## Start the Stack

### Option A: Local Python (fastest for Mon/Tue/demos)
```bash
# Windows PowerShell:
powershell -File scripts/setup.ps1 -Local

# macOS / Linux / Git Bash:
bash scripts/setup.sh --local
```

### Option B: Docker Compose (MLflow UI `:5000` + Fraud API `:8000`)
```bash
# macOS / Linux / Git Bash:
bash scripts/setup.sh

# Windows PowerShell:
powershell -File scripts/setup.ps1
```

Optional Prometheus monitoring (`:9090`):
```bash
docker compose -f docker-compose.yml -f docker-compose.monitoring.yml up -d
```

- **Fraud Console & Dashboard:** [http://localhost:8000](http://localhost:8000)
- **Swagger API Docs:** [http://localhost:8000/docs](http://localhost:8000/docs)
- **MLflow Tracking & Registry UI:** [http://localhost:5000](http://localhost:5000)

Run the test suite:
```bash
pytest tests/ -v
```

## Week 2 PM Schedule & Demo Programs

| Day | Topic & Story Anchor | Module File | Runnable Demos (`demos/`) |
|---|---|---|---|
| **Monday** | ML Lifecycle + MLflow (*The lab notebook*) | [01-monday](course/modules/01-monday-ml-lifecycle-mlflow.md) | `mon_01_unreproducible.py`, `mon_02_mlflow_tracking.py`, `mon_03_registry_promotion.py` |
| **Tuesday** | DVC + Data & Pipeline Versioning (*The time machine for data*) | [02-tuesday](course/modules/02-tuesday-dvc-versioning.md) | `tue_01_dvc_version_rollback.py`, `tue_02_dvc_pipeline_repro.py`, `tue_03_silent_edit_lineage.py` |
| **Wednesday** | Model Deployment: FastAPI + Docker (*The restaurant opens*) | [03-wednesday](course/modules/03-wednesday-deployment-fastapi-docker.md) | `wed_01_fastapi_service.py`, `wed_02_docker_predict.py`, `wed_03_validation_vs_corrupt.py` |
| **Thursday** | Monitoring + Drift Detection (*The lighthouse keeper*) | [04-thursday](course/modules/04-thursday-monitoring-drift.md) | `thu_01_drift_stream.py`, `thu_02_monitoring_readout.py`, `thu_03_alert_tuning.py` |
| **Friday** | Worked Template Build: Fraud Detection (*All 4 anchors*) | [05-friday](course/modules/05-friday-fraud-template-build.md) | Full pipeline (`dvc.yaml` + `fraud_system/` + `break`/`fix` live demo) |
| **Weekend** | No class — Instructor follow-up & self-test | [06-weekend](course/modules/06-weekend-followup-selftest.md) | Closed-book self-test + optional agent catch-up |

## Layout
```
ml-course/
├── fraud_system/        # Production Fraud Detection template (data_gen, features, train, evaluate, monitor, serve)
├── demos/               # 12 <2-min runnable class demos (mon_01..thu_03) with live variation flags
├── tests/               # Automated pytest suite (features, FastAPI serving, drift detection, fault injection)
├── course/modules/      # Mon–Fri instructor playbooks + Weekend follow-up (fixed order + 5A–5D)
├── course/candidate-prompts.md  # Mon–Fri candidate evening rhythm & agent prompts
├── docs/                # Instructor guide, student guide, quickstart, course-toc
├── scripts/             # Cross-platform setup, smoke, break, fix (.sh + .ps1)
├── web/                 # Fraud Detection & Live Drift browser console
├── monitoring/          # Prometheus scrape config
├── .github/workflows/   # GitHub Actions CI workflow (test + Docker build)
├── .claude/skills/      # setup-ml-class, teach-ml-class, setup-candidate, practice-ml
├── dvc.yaml / params.yaml
├── Dockerfile / docker-compose.yml / docker-compose.monitoring.yml
└── requirements.txt / pyproject.toml
```
