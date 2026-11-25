# Class-Day Quick Start (Instructor, 5 Minutes)

## 1. Open `ml-course/` in a NEW AI session
Skills in `.claude/skills/` load at session start.

## 2. Start the stack
- **macOS / Linux / Git Bash:** `bash scripts/setup.sh` (or `--local` for Python-only)
- **Windows PowerShell:** `powershell -File scripts/setup.ps1` (or `-Local` for Python-only)

Wait for **READY**:
- Fraud Console: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- MLflow UI: `http://localhost:5000`

> **macOS note:** If port `5000` is in use by AirPlay Receiver, disable AirPlay Receiver in System Settings or start MLflow on `--port 5001`.

## 3. Run class beat-by-beat
Say **"teach monday"** (or tuesday / wednesday / thursday / friday). Answer **"yes"** if sharing your screen so Exit Check answers stay hidden until you say `answer`.

## 4. Daily Demo Commands at a Glance
| Day | Commands |
|---|---|
| **Mon** | `python demos/mon_01_unreproducible.py`, `mon_02_mlflow_tracking.py`, `mon_03_registry_promotion.py` |
| **Tue** | `python demos/tue_01_dvc_version_rollback.py`, `tue_02_dvc_pipeline_repro.py`, `tue_03_silent_edit_lineage.py` |
| **Wed** | `python demos/wed_01_fastapi_service.py`, `wed_02_docker_predict.py`, `wed_03_validation_vs_corrupt.py` |
| **Thu** | `python demos/thu_01_drift_stream.py`, `thu_02_monitoring_readout.py`, `thu_03_alert_tuning.py` |
| **Fri** | `dvc repro` -> `pytest tests/ -v` -> `scripts/break.sh data-drift` -> `scripts/fix.sh` |
