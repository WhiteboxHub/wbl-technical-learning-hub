#!/usr/bin/env bash
# Undo any injected Docker fault and restore the healthy Cargo Manifest stack.
set -euo pipefail
cd "$(dirname "$0")/.."

docker compose unpause redis >/dev/null 2>&1 || true
rm -f .fault-override.yml
docker compose up -d --force-recreate >/dev/null 2>&1

for _ in $(seq 1 30); do
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    echo "all faults cleared (healthy baseline restored: harbor-api + harbor-redis)"
    exit 0
  fi
  sleep 1
done

echo "warning: stack restarted, but /health did not respond within 30s (check: docker compose logs)"
exit 1

