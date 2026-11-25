---
name: setup-candidate
description: Candidate laptop setup for Week 2 PM Production ML across Windows, Mac, and Linux. Use when a student says "set up my environment", "my python or docker setup failed", or needs to run demos locally.
---

# Candidate Setup — Week 2 PM Production ML

Get the candidate's machine ready so every task and demo runs locally (no cloud account required).

## Steps
1. Detect OS (Windows PowerShell, macOS, or Linux/WSL2).
2. Recommend either **local Python `.venv`** (`scripts/setup.ps1 -Local` on Windows or `scripts/setup.sh --local` on macOS/Linux) or **Docker Compose** (`scripts/setup.ps1` / `scripts/setup.sh`).
3. Verify each step in order:
   - `python --version` (3.10+)
   - `git --version`
   - `python -m fraud_system.data_gen --version v1 --out data/transactions.csv`
   - `python -m fraud_system.train --data data/transactions.csv --params params.yaml`
   - `pytest tests/ -v`
4. Diagnose top setup failures cleanly (Python PATH/Store alias on Windows, Docker daemon not running, port 5000/8000 already bound — e.g. macOS AirPlay Receiver on port 5000!).

## Rules
- Explain each failure in plain language before fixing.
- Never edit answer keys or complete candidate assignments during setup.
