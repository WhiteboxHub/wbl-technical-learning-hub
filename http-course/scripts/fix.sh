#!/usr/bin/env bash
# Undo every injected fault and return to the healthy capstone baseline (CORS on for the web page, auth off).
cd "$(dirname "$0")/.."
F="-f docker-compose.yml -f docker-compose.cors.yml"
SPLIT="-f docker-compose.yml -f docker-compose.split.yml"
docker compose $SPLIT unpause departments-service >/dev/null 2>&1 || true
rm -f .fault-override.yml gateway/.fault.conf
docker compose $F up -d --force-recreate api gateway >/dev/null 2>&1
docker compose exec -T redis redis-cli DEL departments:list >/dev/null 2>&1
for _ in $(seq 1 30); do curl -sf http://localhost:8000/health >/dev/null && break; sleep 1; done
echo "all faults cleared (baseline: monolith API + gateway + CORS on, auth off)"
