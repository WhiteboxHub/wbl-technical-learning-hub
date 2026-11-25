#!/usr/bin/env bash
# Restores System Design stack to healthy baseline
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

echo "Clearing all faults and restoring healthy baseline..."

# Remove fault overrides if any
rm -f .fault-override.yml gateway/.fault.conf

# Unpause worker if paused
docker compose unpause worker >/dev/null 2>&1 || true

# Start all containers in healthy baseline mode
docker compose -f docker-compose.yml up -d --force-recreate >/dev/null 2>&1

# Wait for health
echo "Verifying health..."
for i in $(seq 1 20); do
  if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
    echo "Stack restored to healthy state."
    exit 0
  fi
  sleep 1
done

echo "Warning: Could not verify health immediately. Run scripts/smoke.sh to check."
