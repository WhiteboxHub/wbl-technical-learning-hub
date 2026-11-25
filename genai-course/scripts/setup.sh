#!/usr/bin/env bash
# One-command setup for the GenAI & RAG course stack.
#   scripts/setup.sh           check prerequisites, start the stack, run the smoke test
#   scripts/setup.sh --reset   wipe vector database volume first (back to clean seed data)
#   scripts/setup.sh --stop    stop the stack
#
# Exit codes: 0 ok | 10 docker missing | 11 docker daemon not running | 12 port in use
#             13 API never became healthy | 14 smoke test failed | 15 curl missing
#             16 OPENAI_API_KEY missing or invalid in .env
set -u
cd "$(dirname "$0")/.."

say()  { printf '%s\n' "$*"; }
step() { printf '\n== %s\n' "$*"; }

if [ "${1:-}" = "--stop" ]; then
  say "Stopping GenAI course stack..."
  docker compose down
  exit 0
fi

step "Checking prerequisites"
command -v docker >/dev/null 2>&1 || { say "ERROR: docker not found. Install Docker Desktop: https://www.docker.com/products/docker-desktop/"; exit 10; }
docker compose version >/dev/null 2>&1 || { say "ERROR: 'docker compose' (v2) not found. Update Docker Desktop."; exit 10; }
command -v curl >/dev/null 2>&1 || { say "ERROR: curl not found. Please install curl."; exit 15; }
docker info >/dev/null 2>&1 || { say "ERROR: Docker is installed but not running. Start Docker Desktop and wait until it is running."; exit 11; }
say "docker $(docker --version | sed 's/Docker version //; s/,.*//'), compose ok, curl ok, daemon running"

step "Checking environment configuration (.env)"
if [ ! -f .env ]; then
  if [ -f .env.example ]; then
    say "Warning: .env not found. Copying .env.example to .env..."
    cp .env.example .env
  else
    touch .env
  fi
fi

# Check for OPENAI_API_KEY
API_KEY=$(grep -E '^OPENAI_API_KEY=' .env 2>/dev/null | cut -d '=' -f2- | tr -d ' "' || true)
if [ -z "$API_KEY" ] || [ "$API_KEY" = "sk-placeholder-replace-with-real-key" ] || [ "$API_KEY" = "your-api-key-here" ]; then
  say "ERROR: Valid OPENAI_API_KEY not configured in .env."
  say "Please open .env and set: OPENAI_API_KEY=sk-..."
  say "A real key is required for OpenAI embeddings and completions."
  exit 16
fi
say "OPENAI_API_KEY is configured"

if [ "${1:-}" = "--reset" ]; then
  step "Resetting (removing containers and ChromaDB vector database volume)"
  docker compose down -v
fi

step "Checking ports 3000 (UI), 8000 (API), 8001 (ChromaDB)"
ours=$(docker compose ps --status running -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$ours" = "0" ]; then
  for port in 3000 8000 8001; do
    if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
      say "ERROR: port $port is already in use by another program:"
      lsof -nP -iTCP:"$port" -sTCP:LISTEN | sed -n '1,3p'
      say "Stop that program (or free the port) and re-run."
      exit 12
    fi
  done
  say "ports 3000, 8000, 8001 free"
else
  say "course stack already running; will update it"
fi

step "Building and starting the stack (first run can take 2-3 minutes)"
docker compose up --build -d || { say "ERROR: docker compose up failed. Run 'docker compose logs' for details."; exit 13; }

step "Waiting for ChromaDB and FastAPI services"
for _ in $(seq 1 45); do
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    break
  fi
  sleep 2
done

if ! curl -sf http://localhost:8000/health >/dev/null 2>&1; then
  say "ERROR: API did not become healthy within 90s. Last logs:"
  docker compose logs --tail 30 api
  exit 13
fi
say "API and ChromaDB are healthy"

step "Running smoke test"
if scripts/smoke.sh; then
  step "READY"
  say "API:         http://localhost:8000"
  say "Swagger UI:  http://localhost:8000/docs"
  say "ChromaDB:    http://localhost:8001"
  say "UI Explorer: http://localhost:8501 (or http://localhost:3000)"
  say ""
  say "Reset data:  scripts/setup.sh --reset"
  say "Stop stack:  scripts/setup.sh --stop"
  exit 0
fi

say "ERROR: smoke test failed. See FAIL lines above; check 'docker compose logs api'."
exit 14
