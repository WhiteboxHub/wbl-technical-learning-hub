#!/usr/bin/env bash
# Undo every injected fault and return to the healthy baseline.
# Baseline: standard recursive chunking (512/64), clean HR policy corpus, temperature 0.2, text-embedding-3-small.
set -e
cd "$(dirname "$0")/.."

API="${API_URL:-http://localhost:8000}"

echo "Restoring GenAI course stack to baseline..."

# 1. Delete poisoned documents if present in ChromaDB
curl -s -X DELETE "$API/documents/poisoned-pto-update" >/dev/null 2>&1 || true
curl -s -X DELETE "$API/documents/fake-tesla-benefit" >/dev/null 2>&1 || true

# 2. Remove any fault compose overrides
rm -f .fault-override.yml

# 3. Recreate the API container cleanly with baseline docker-compose.yml
docker compose up -d --force-recreate api >/dev/null 2>&1

# 4. Wait for API recovery
for _ in $(seq 1 30); do
  if curl -sf "$API/health" >/dev/null 2>&1; then
    break
  fi
  sleep 1
done

# 5. Reseed baseline HR documents if needed
curl -s -X POST "$API/ingest" \
  -H "Content-Type: application/json" \
  -d '{"document_id":"pto-and-leave-policy.md","text":"Meridian Solutions provides full-time employees with 18 days of paid time off (PTO) per calendar year. PTO accrues on a monthly basis at a rate of 1.5 days per month.","metadata":{"source":"pto-and-leave-policy.md"}}' >/dev/null 2>&1 || true

echo "All faults cleared (baseline: standard chunking, temperature 0.2, authentic HR documents)."
