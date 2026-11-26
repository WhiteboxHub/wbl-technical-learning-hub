#!/usr/bin/env bash
# One-command setup for the Unix & Shell Scripting lab container (Ubuntu 24.04).
#   scripts/setup.sh           check prerequisites, build & start wbl-unix, run smoke test
#   scripts/setup.sh --reset   wipe lab volume & recreate fresh seeded workspace
#   scripts/setup.sh --stop    stop the container
#
# Exit codes: 0 ok | 10 docker missing | 11 docker daemon not running | 12 port 8085 in use
#             13 container never became healthy | 14 smoke test failed | 15 curl missing
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
  step "Resetting (removing container and lab volume)"
  docker compose down -v
fi

step "Checking port 8085"
ours=$(docker compose ps --status running -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$ours" = "0" ]; then
  if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:8085 -sTCP:LISTEN >/dev/null 2>&1; then
    say "ERROR: port 8085 is already in use by another program:"
    lsof -nP -iTCP:8085 -sTCP:LISTEN | sed -n '1,3p'
    say "Stop that program (or free port 8085) and re-run."
    exit 12
  fi
  say "port 8085 free"
else
  say "unix lab container already running; will ensure it is up to date"
fi

step "Building and starting Ubuntu 24.04 Unix Lab (first run builds image)"
docker compose up -d --build || { say "ERROR: docker compose failed. Run 'docker compose logs' for details."; exit 13; }

step "Waiting for Unix Lab workspace to become seeded and healthy"
ready=0
for _ in $(seq 1 40); do
  if docker compose exec -T unix test -f /workspace/training_lab/.seeded >/dev/null 2>&1; then
    cnt=$(docker compose exec -T unix wc -l /workspace/training_lab/logs/app.log 2>/dev/null | awk '{print $1}' | tr -d '\r' || echo 0)
    if [ "${cnt:-0}" -ge 120 ] 2>/dev/null; then
      ready=1
      break
    fi
  fi
  sleep 2
done

if [ "$ready" -ne 1 ]; then
  say "ERROR: Unix Lab did not become ready within 80s. Last logs:"
  docker compose logs --tail 30 unix
  exit 13
fi
say "Unix Lab is up and seeded"

step "Smoke test"
if scripts/smoke.sh; then
  step "READY"
  say "Workspace: /workspace/training_lab  (inside container: wbl-unix)"
  say "Shell CLI: scripts/sh.sh \"pwd && ls -la\""
  say "Open Bash: scripts/sh.sh"
  say "Lab HTTP:  http://localhost:8085  (serves /workspace/training_lab/docs for curl/netstat checks)"
  say "Reset:     scripts/setup.sh --reset      Stop: scripts/setup.sh --stop"
  exit 0
fi
say "ERROR: smoke test failed. See FAIL lines above; 'docker compose logs unix' may explain."
exit 14
