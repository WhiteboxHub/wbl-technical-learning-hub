#!/usr/bin/env bash
set -euo pipefail

BASE_URL="${1:-http://localhost:8000}"
CODE="TEST$(date +%s)"

echo "1. Checking /health at ${BASE_URL}..."
curl -fsS "${BASE_URL}/health"
echo ""

echo "2. Creating container ${CODE}..."
CREATED_JSON=$(curl -fsS -X POST "${BASE_URL}/containers" \
  -H "Content-Type: application/json" \
  -d "{\"container_code\":\"${CODE}\",\"cargo\":\"Turbine Parts\",\"origin_port\":\"Busan\",\"destination_port\":\"Rotterdam\",\"weight_kg\":14200,\"status\":\"docked\"}")
echo "${CREATED_JSON}"

echo "3. Listing containers..."
curl -fsS "${BASE_URL}/containers" | head -c 300
echo ""

echo "4. Checking /stats..."
curl -fsS "${BASE_URL}/stats"
echo ""
echo "Smoke check passed!"
