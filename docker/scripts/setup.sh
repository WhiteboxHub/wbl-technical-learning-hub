#!/usr/bin/env bash
# One-command setup for the Docker ("The Shipping Container") course stack.
#   scripts/setup.sh           check prerequisites, start the stack, run the smoke test
#   scripts/setup.sh --reset   wipe volumes first (fresh manifest.db and redis)
#   scripts/setup.sh --stop    stop the stack
#
# Exit codes: 0 ok | 10 docker missing | 11 docker daemon not running | 12 port in use
#             13 API never became healthy | 14 smoke test failed | 15 curl missing
set -u
cd "$(dirname "$0")/.."

say()  { printf '%s\n' "$*"; }
step() { printf '\n== %s\n' "$*"; }

if [ "${1:-}" = "--stop" ]; then docker compose down; exit 0; fi

step "Checking prerequisites"
command -v docker >/dev/null 2>&1 || { say "ERROR: docker not found. Install Docker Desktop: https://www.docker.com/products/docker-desktop/"; exit 10; }
docker compose version >/dev/null 2>&1 || { say "ERROR: 'docker compose' (v2) not found. Update Docker Desktop."; exit 10; }
command -v curl >/dev/null 2>&1 || { say "ERROR: curl not found."; exit 15; }
docker info >/dev/null 2>&1 || { say "ERROR: Docker is installed but not running. Start Docker Desktop and wait until it says it is running, then re-run."; exit 11; }
say "docker $(docker --version | sed 's/Docker version //; s/,.*//'), compose ok, curl ok, daemon running"

if [ "${1:-}" = "--reset" ]; then
  step "Resetting (removing containers and named volumes)"
  docker compose down -v
fi

step "Checking port 8000"
ours=$(docker compose ps --status running -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$ours" = "0" ]; then
  if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:8000 -sTCP:LISTEN >/dev/null 2>&1; then
    say "ERROR: port 8000 is already in use by another program:"
    lsof -nP -iTCP:8000 -sTCP:LISTEN | sed -n '1,3p'
    say "Stop that program (or run 'docker compose down' in another course) and re-run."
    exit 12
  fi
  say "port 8000 free"
else
  say "course stack already running; will update it"
fi

step "Building and starting the stack"
docker compose up --build -d || { say "ERROR: docker compose failed. Run 'docker compose logs' for details."; exit 13; }

step "Waiting for the Cargo Manifest API"
for _ in $(seq 1 30); do
  curl -sf http://localhost:8000/health >/dev/null 2>&1 && break
  sleep 2
done
if ! curl -sf http://localhost:8000/health >/dev/null 2>&1; then
  say "ERROR: API did not become healthy within 60s. Last logs:"
  docker compose logs --tail 30 api
  exit 13
fi
say "API is up"

step "Running smoke test"
if ./scripts/smoke.sh; then
  step "READY"
  say "API:      http://localhost:8000/containers"
  say "Swagger:  http://localhost:8000/docs"
  say "Health:   http://localhost:8000/health"
  say "Stats:    http://localhost:8000/stats"
  say "Tests:    docker compose exec api pytest -q"
  say "Reset:    ./scripts/setup.sh --reset      Stop: ./scripts/setup.sh --stop"
  exit 0
fi
say "ERROR: smoke test failed. Check 'docker compose logs api'."
exit 14
