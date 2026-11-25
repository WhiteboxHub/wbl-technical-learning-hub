#!/usr/bin/env bash
cd "$(dirname "$0")/.."
BASE="${BASE:-http://localhost:8000}"
echo '{}' > .fault_state.json
curl -sf -X POST "$BASE/v1/monitor/reset" >/dev/null 2>&1 || true
echo "faults cleared; baseline Fraud Detection API restored"
