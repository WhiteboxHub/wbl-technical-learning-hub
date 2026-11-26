#!/usr/bin/env bash
# One-command setup for the MySQL course stack (Training Management DB).
#   scripts/setup.sh           check prerequisites, start MySQL + Adminer + Redis, run smoke test
#   scripts/setup.sh --reset   wipe database volume first (back to seed data)
#   scripts/setup.sh --stop    stop the stack
#
# Exit codes: 0 ok | 10 docker missing | 11 docker daemon not running | 12 port in use
#             13 MySQL never became healthy | 14 smoke test failed | 15 curl missing
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
  step "Resetting (removing containers and database volume)"
  docker compose down -v
fi

step "Checking ports 3306, 8082, and 6379"
ours=$(docker compose ps --status running -q 2>/dev/null | wc -l | tr -d ' ')
if [ "$ours" = "0" ]; then
  for port in 3306 8082 6379; do
    if command -v lsof >/dev/null 2>&1 && lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; then
      say "ERROR: port $port is already in use by another program:"
      lsof -nP -iTCP:"$port" -sTCP:LISTEN | sed -n '1,3p'
      say "Stop that program (or free the port) and re-run."
      exit 12
    fi
  done
  say "ports free"
else
  say "course stack already running; will update it"
fi

step "Starting MySQL 8.0, Adminer, and Redis (first run downloads images, can take a few minutes)"
docker compose up -d || { say "ERROR: docker compose failed. Run 'docker compose logs' for details."; exit 13; }

step "Waiting for MySQL to become healthy and seeded"
ready=0
for _ in $(seq 1 45); do
  if docker compose exec -T mysql mysqladmin ping -h localhost -uroot -proot --silent >/dev/null 2>&1; then
    cnt=$(docker compose exec -T mysql mysql -N -uroot -proot -D training_db -e "SELECT COUNT(*) FROM activity_log;" 2>/dev/null | tr -d '\r' | tail -n 1 || echo 0)
    if [ "${cnt:-0}" -ge 2000 ] 2>/dev/null; then
      ready=1
      break
    fi
  fi
  sleep 2
done

if [ "$ready" -ne 1 ]; then
  say "ERROR: MySQL did not become healthy and seeded within 90s. Last logs:"
  docker compose logs --tail 30 mysql
  exit 13
fi
say "MySQL is up and seeded"

step "Smoke test"
if scripts/smoke.sh; then
  step "READY"
  say "MySQL:    localhost:3306  (db: training_db | user: root | pass: root)"
  say "Adminer:  http://localhost:8082  (System: MySQL, Server: mysql, User: root, Pass: root, DB: training_db)"
  say "Redis:    localhost:6379  (Module 4 cache-aside demo)"
  say "SQL CLI:  scripts/sql.sh \"SELECT * FROM student;\""
  say "Reset:    scripts/setup.sh --reset      Stop: scripts/setup.sh --stop"
  exit 0
fi
say "ERROR: smoke test failed. See FAIL lines above; 'docker compose logs mysql' may explain."
exit 14
