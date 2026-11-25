#!/usr/bin/env bash
set -u
BASE="${1:-http://localhost:8000}"
fail=0

check() {
  local label="$1" want="$2" method="$3" path="$4" body="${5:-}" got
  if [ -n "$body" ]; then
    got=$(curl -s -o /tmp/ml_smoke -w "%{http_code}" -X "$method" "$BASE$path" -H "Content-Type: application/json" -d "$body")
  else
    got=$(curl -s -o /tmp/ml_smoke -w "%{http_code}" -X "$method" "$BASE$path")
  fi
  if [ "$got" = "$want" ]; then echo "PASS  $label ($got)"; else echo "FAIL  $label: wanted $want, got $got"; fail=1; fi
}

VALID='{"amount":1250,"hour_of_day":2,"merchant_risk_score":0.85,"tx_velocity_24h":5,"distance_from_home_km":180,"is_international":1,"card_present":0,"account_age_days":45}'
INVALID='{"amount":-50,"hour_of_day":28}'

check "health endpoint"       200 GET  /health
check "model info"            200 GET  /v1/model-info
check "valid prediction"      200 POST /v1/predict "$VALID"
check "validation error"      422 POST /v1/predict "$INVALID"
check "drift monitor summary" 200 GET  /v1/monitor/drift
check "prometheus metrics"    200 GET  /metrics

[ $fail -eq 0 ] && echo "ALL SMOKE CHECKS PASSED" || { echo "SMOKE CHECKS FAILED"; exit 1; }
