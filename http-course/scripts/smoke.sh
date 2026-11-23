#!/usr/bin/env bash
# Smoke test for the HR API. Usage: scripts/smoke.sh [base_url]
BASE="${1:-http://localhost:8000}"
WEB="${2:-http://localhost:3000}"
fail=0
EMAIL="smoke.$RANDOM$RANDOM@example.com"

check() {  # check <label> <expected_status> <method> <path> [json_body]
  local label="$1" want="$2" method="$3" path="$4" body="$5" got
  if [ -n "$body" ]; then
    got=$(curl -s -o /tmp/smoke_body -w "%{http_code}" -X "$method" "$BASE$path" -H "Content-Type: application/json" -d "$body")
  else
    got=$(curl -s -o /tmp/smoke_body -w "%{http_code}" -X "$method" "$BASE$path")
  fi
  if [ "$got" = "$want" ]; then echo "PASS  $label ($got)"; else echo "FAIL  $label: wanted $want, got $got"; fail=1; fi
}

NEW="{\"name\":\"Smoke Test\",\"email\":\"$EMAIL\",\"title\":\"Tester\",\"department_id\":2,\"manager_id\":2,\"hire_date\":\"2024-01-15\",\"salary\":90000}"
UPD="{\"name\":\"Smoke Updated\",\"email\":\"$EMAIL\",\"title\":\"Senior Tester\",\"department_id\":2,\"manager_id\":2,\"hire_date\":\"2024-01-15\",\"salary\":95000}"

check "health"                         200 GET    /health
check "list departments"               200 GET    /v2/departments
check "list employees"                 200 GET    /v2/employees
check "get employee 1"                 200 GET    /v2/employees/1
check "employees of department 2"      200 GET    /v2/departments/2/employees
check "unknown employee"               404 GET    /v2/employees/99999
check "create employee"                201 POST   /v2/employees "$NEW"
ID=$(sed -n 's/.*"id":\([0-9]*\).*/\1/p' /tmp/smoke_body | head -1)
check "duplicate email"                409 POST   /v2/employees "$NEW"
check "invalid body"                   422 POST   /v2/employees '{"name":"x"}'
check "bad department reference"       422 POST   /v2/employees "${NEW/\"department_id\":2/\"department_id\":999}"
check "replace employee (PUT)"         200 PUT    /v2/employees/$ID "$UPD"
check "partial update (PATCH)"         200 PATCH  /v2/employees/$ID '{"title":"Lead Tester"}'
check "delete employee"                204 DELETE /v2/employees/$ID
check "deleted employee is gone"       404 GET    /v2/employees/$ID
check "method not allowed"             405 DELETE /v2/employees
check "department in use can't be deleted" 409 DELETE /v2/departments/2

got=$(curl -s -o /dev/null -w "%{http_code}" "$WEB/")
if [ "$got" = "200" ]; then echo "PASS  web directory page ($got)"; else echo "FAIL  web directory page: wanted 200, got $got"; fail=1; fi
JAR=$(mktemp)
curl -s -c "$JAR" "$BASE/demo/cookie" -o /dev/null
if grep -q "session_id" "$JAR" && grep -q "theme" "$JAR"; then echo "PASS  demo cookies set (session_id, theme)"; else echo "FAIL  demo cookies not set"; fail=1; fi
if curl -s -b "$JAR" "$BASE/demo/whoami" | grep -q session_id; then echo "PASS  whoami echoes cookies"; else echo "FAIL  whoami did not echo cookies"; fail=1; fi
rm -f "$JAR"

GW="${GATEWAY:-http://localhost:8080}"
if curl -si "$GW/health" | grep -qi "x-request-id"; then echo "PASS  gateway answers with X-Request-Id"; else echo "FAIL  gateway not answering"; fail=1; fi
curl -s -o /dev/null "$BASE/v2/departments"
if curl -si "$BASE/v2/departments" | grep -qi "x-cache-status: HIT"; then echo "PASS  redis cache (HIT on second read)"; else echo "FAIL  redis cache not working"; fail=1; fi

echo
if [ $fail -eq 0 ]; then echo "ALL CHECKS PASSED"; else echo "SOME CHECKS FAILED"; exit 1; fi
