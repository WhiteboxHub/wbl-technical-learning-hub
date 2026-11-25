#!/usr/bin/env bash
# One-command setup for Week 2 PM Production ML course.
#   scripts/setup.sh          check prerequisites, prepare baseline, start Docker stack, smoke test
#   scripts/setup.sh --local  set up Python .venv locally without Docker
#   scripts/setup.sh --stop   stop Docker containers
set -u
cd "$(dirname "$0")/.."

say()  { printf '%s\n' "$*"; }
step() { printf '\n== %s\n' "$*"; }

if [ "${1:-}" = "--stop" ]; then docker compose down; exit 0; fi

if [ "${1:-}" = "--local" ]; then
  step "Setting up local Python virtual environment (.venv)"
  python3 -m venv .venv || python -m venv .venv || { say "ERROR: python not found"; exit 10; }
  . .venv/bin/activate
  pip install -r requirements.txt
  python -m fraud_system.data_gen --version v1 --out data/transactions.csv
  python -m fraud_system.train --data data/transactions.csv --params params.yaml
  say "READY (local venv). Start API: uvicorn fraud_system.serve:app --port 8000"
  exit 0
fi

step "Checking prerequisites"
command -v docker >/dev/null 2>&1 || { say "ERROR: docker not found (exit 10)"; exit 10; }
docker compose version >/dev/null 2>&1 || { say "ERROR: docker compose v2 not found (exit 10)"; exit 10; }
command -v curl >/dev/null 2>&1 || { say "ERROR: curl not found (exit 15)"; exit 15; }
docker info >/dev/null 2>&1 || { say "ERROR: Docker daemon is not running (exit 11)"; exit 11; }

touch .fault_state.json
echo '{}' > .fault_state.json

step "Starting MLflow (:5000) and Fraud API (:8000)"
docker compose up --build -d || { say "ERROR: docker compose failed (exit 13)"; exit 13; }

step "Waiting for Fraud API"
for _ in $(seq 1 40); do
  curl -sf http://localhost:8000/health >/dev/null 2>&1 && break
  sleep 2
done

scripts/smoke.sh || exit 14
step "READY"
say "Fraud Console : http://localhost:8000"
say "Swagger Docs  : http://localhost:8000/docs"
say "MLflow UI     : http://localhost:5000"
say "Stop          : scripts/setup.sh --stop"
