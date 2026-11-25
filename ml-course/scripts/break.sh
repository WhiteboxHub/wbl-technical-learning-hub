#!/usr/bin/env bash
# Capstone & Thursday fault injector.
# Usage: scripts/break.sh data-drift | concept-drift | bad-schema | latency-spike
set -e
cd "$(dirname "$0")/.."
BASE="${BASE:-http://localhost:8000}"

case "${1:-}" in
  data-drift)
    echo '{"fault":"data-drift"}' > .fault_state.json
    curl -sf -X POST "$BASE/v1/monitor/simulate" -H "Content-Type: application/json" -d '{"n":120,"data_drift":true,"seed":202}' >/dev/null
    echo "fault injected: data-drift (check GET /v1/monitor/drift)" ;;
  concept-drift)
    echo '{"fault":"concept-drift"}' > .fault_state.json
    curl -sf -X POST "$BASE/v1/monitor/simulate" -H "Content-Type: application/json" -d '{"n":120,"data_drift":false,"concept_drift":true,"seed":303}' >/dev/null
    echo "fault injected: concept-drift (check live fraud rate vs ref)" ;;
  bad-schema)
    echo '{"fault":"bad-schema"}' > .fault_state.json
    echo "fault injected: bad-schema (POST /v1/predict now returns 500 schema error)" ;;
  latency-spike)
    echo '{"fault":"latency-spike"}' > .fault_state.json
    echo "fault injected: latency-spike (POST /v1/predict delayed >250ms)" ;;
  *)
    echo "usage: scripts/break.sh data-drift|concept-drift|bad-schema|latency-spike"; exit 1 ;;
esac
