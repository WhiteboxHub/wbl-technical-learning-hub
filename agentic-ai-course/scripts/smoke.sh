#!/usr/bin/env bash
set -e

BASE_URL="http://localhost:8000"
echo "=== ClaimFlow AI Smoke Test Suite ==="

# 1. Health check
echo -n "1. Checking API Health... "
HEALTH=$(curl -s "$BASE_URL/health")
if [[ "$HEALTH" == *"healthy"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL] - API response: $HEALTH"
    exit 1
fi

# 2. Patient List
echo -n "2. Querying Patient Roster... "
PATIENTS=$(curl -s "$BASE_URL/api/v1/patients")
if [[ "$PATIENTS" == *"PAT-901"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL]"
    exit 1
fi

# 3. Model Context Protocol Tools
echo -n "3. Inspecting MCP Tool Schemas... "
MCP=$(curl -s "$BASE_URL/api/v1/mcp/tools")
if [[ "$MCP" == *"check_eligibility"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL]"
    exit 1
fi

# 4. Standard Claim Auto-Approval ($800)
echo -n "4. Submitting Low-Dollar Claim (Auto-Approval Expected)... "
RESP_AUTO=$(curl -s -X POST "$BASE_URL/api/v1/claims" \
  -H "Content-Type: application/json" \
  -d '{"claim_id":"SMOKE-AUTO-01","patient_id":"PAT-901","patient_name":"John Doe","provider_id":"PRV-501","diagnosis_code":"M17.11","procedure_code":"27447","requested_amount":800.0,"clinical_notes":"Documented severe osteoarthritis failing conservative therapy","tenant_id":"tenant-health-corp"}')

if [[ "$RESP_AUTO" == *"approved"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL] - $RESP_AUTO"
    exit 1
fi

# 5. Ineligible Patient Denial
echo -n "5. Submitting Ineligible Patient Claim (Denial Expected)... "
RESP_INELIGIBLE=$(curl -s -X POST "$BASE_URL/api/v1/claims" \
  -H "Content-Type: application/json" \
  -d '{"claim_id":"SMOKE-INELIGIBLE-01","patient_id":"PAT-903","patient_name":"Robert Miller","provider_id":"PRV-501","diagnosis_code":"M17.11","procedure_code":"27447","requested_amount":500.0,"clinical_notes":"Routine checkup","tenant_id":"tenant-health-corp"}')

if [[ "$RESP_INELIGIBLE" == *"denied"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL] - $RESP_INELIGIBLE"
    exit 1
fi

# 6. High-Dollar Human Approval Gate ($14,000)
echo -n "6. Submitting High-Dollar Claim (HITL Approval Gate Expected)... "
RESP_HITL=$(curl -s -X POST "$BASE_URL/api/v1/claims" \
  -H "Content-Type: application/json" \
  -d '{"claim_id":"SMOKE-HITL-01","patient_id":"PAT-901","patient_name":"John Doe","provider_id":"PRV-501","diagnosis_code":"M17.11","procedure_code":"27447","requested_amount":14000.0,"clinical_notes":"Complete joint arthroplasty","tenant_id":"tenant-health-corp"}')

if [[ "$RESP_HITL" == *"pending_human_approval"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL] - $RESP_HITL"
    exit 1
fi

# 7. Resolving Human Review Gate
echo -n "7. Resolving HITL Review Gate... "
RESP_RESOLVE=$(curl -s -X POST "$BASE_URL/api/v1/claims/SMOKE-HITL-01/human-review" \
  -H "Content-Type: application/json" \
  -d '{"decision":"approve","human_notes":"Authorized after orthopedics surgical consult review","approved_amount":14000.0}')

if [[ "$RESP_RESOLVE" == *"approved"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL] - $RESP_RESOLVE"
    exit 1
fi

# 8. Web UI Asset Serving
echo -n "8. Checking Web UI Index... "
INDEX=$(curl -s "$BASE_URL/")
if [[ "$INDEX" == *"ClaimFlow AI"* ]]; then
    echo "[PASS]"
else
    echo "[FAIL]"
    exit 1
fi

echo "All smoke tests completed with 100% success."
