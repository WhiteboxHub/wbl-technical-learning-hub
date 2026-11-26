#!/usr/bin/env bash
# Capstone fault injector (Module 5). Usage: ./scripts/break.sh <fault>   Undo everything: ./scripts/fix.sh
# Faults: loopback-bind | localhost-redis | readonly-data | redis-down
# The instructor runs this; candidates diagnose from evidence (docker ps, docker logs, curl) before fixing.
set -euo pipefail
cd "$(dirname "$0")/.."

wait_api() {
  for _ in $(seq 1 20); do
    if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
      return 0
    fi
    sleep 1
  done
  return 0
}

case "${1:-}" in
  loopback-bind)
    # Container runs uvicorn on 127.0.0.1 instead of 0.0.0.0: host port mapping fails
    cat > .fault-override.yml <<'YAML'
services:
  api:
    command: ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
YAML
    docker compose -f docker-compose.yml -f .fault-override.yml up -d --force-recreate api >/dev/null 2>&1
    sleep 2
    echo "fault injected: loopback-bind (container is Up, but uvicorn binds 127.0.0.1 inside the box)"
    ;;
  localhost-redis)
    # API uses localhost instead of service name 'redis' on harbor-net
    cat > .fault-override.yml <<'YAML'
services:
  api:
    environment:
      REDIS_URL: "redis://localhost:6379/0"
YAML
    docker compose -f docker-compose.yml -f .fault-override.yml up -d --force-recreate api >/dev/null 2>&1
    wait_api
    echo "fault injected: localhost-redis (API points REDIS_URL at localhost instead of redis:6379)"
    ;;
  readonly-data)
    # Named volume mounted read-only: GET works, POST /containers fails writing /data/manifest.db
    cat > .fault-override.yml <<'YAML'
services:
  api:
    volumes:
      - cargo-data:/data:ro
YAML
    docker compose -f docker-compose.yml -f .fault-override.yml up -d --force-recreate api >/dev/null 2>&1
    wait_api
    echo "fault injected: readonly-data (cargo-data mounted :ro at /data; writes fail)"
    ;;
  redis-down)
    # Redis container paused on harbor-net
    docker compose pause redis >/dev/null 2>&1
    echo "fault injected: redis-down (harbor-redis is paused)"
    ;;
  *)
    echo "usage: ./scripts/break.sh loopback-bind|localhost-redis|readonly-data|redis-down"
    exit 1
    ;;
esac

