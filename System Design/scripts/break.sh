#!/usr/bin/env bash
# System Design Fault Injector
# Injects real production failure modes for candidates to diagnose:
# 1. redis-down      -> Cache & Queues crash, requests fallback to DB with high latency
# 2. db-bottleneck   -> Database queries blocked/delayed by 1.5s
# 3. rate-limit      -> Gateway rate-limits every incoming request
# 4. queue-backlog   -> Worker is stopped, queue piles up indefinitely

set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

case "${1:-}" in
  redis-down)
    echo "Injecting fault: Stopping Redis container (Corner shop closed)..."
    docker compose stop redis >/dev/null 2>&1
    echo "Fault injected: Redis is down. Reads fallback to DB, queues paused."
    ;;
  db-bottleneck)
    echo "Injecting fault: Simulating severe DB locking and disk I/O delay (1.5s per query)..."
    docker compose -f docker-compose.yml -f docker-compose.nocache.yml up -d api >/dev/null 2>&1
    echo "Fault injected: DB delay active. Latency will spike to >1500ms."
    ;;
  rate-limit)
    echo "Injecting fault: Tightening rate limit zone to 1 request per minute..."
    sed 's#rate=10r/m;#rate=1r/m;#' gateway/nginx.conf > gateway/.fault.conf
    printf 'services:\n  gateway:\n    volumes:\n      - ./gateway/.fault.conf:/etc/nginx/conf.d/default.conf:ro\n' > .fault-override.yml
    docker compose -f docker-compose.yml -f .fault-override.yml up -d --force-recreate gateway >/dev/null 2>&1
    echo "Fault injected: Harsh rate limiting active. 429 Too Many Requests will trigger immediately."
    ;;
  queue-backlog)
    echo "Injecting fault: Pausing background queue worker (Depot workers on strike)..."
    docker compose pause worker >/dev/null 2>&1
    echo "Fault injected: Worker paused. Async writes and analytics queue will build up in memory."
    ;;
  *)
    echo "Usage: scripts/break.sh <fault>"
    echo "Fault options: redis-down | db-bottleneck | rate-limit | queue-backlog"
    echo "To restore healthy baseline: scripts/fix.sh"
    exit 1
    ;;
esac
