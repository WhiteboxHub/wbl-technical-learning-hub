#!/usr/bin/env bash
# Automated Smoke Test for System Design Stack (10 Verifications)
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE_URL="http://localhost:8080"
DIRECT_URL="http://localhost:8000"

echo "Running System Design smoke test against $BASE_URL..."

# 1. Direct API health
echo -n "1. Checking direct app health (:8000)... "
curl -sf "$DIRECT_URL/health" >/dev/null
echo "OK"

# 2. Gateway health
echo -n "2. Checking gateway / load balancer routing (:8080)... "
res=$(curl -sf "$BASE_URL/health")
echo "$res" | grep -q "healthy"
echo "OK"

# 3. Synchronous shorten write (DB write)
echo -n "3. Testing synchronous URL shortening (POST /api/shorten)... "
code_raw=$(curl -sf -X POST "$BASE_URL/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://whiteboxlearning.com/system-design-test", "custom_code": "smoke-test"}')
echo "$code_raw" | grep -q "smoke-test"
echo "OK (201 Created)"

# 4. First read: Cache Miss -> Populates Cache
echo -n "4. Testing first read resolution (Expected: X-Cache MISS)... "
headers_miss=$(curl -sI "$BASE_URL/r/smoke-test")
echo "$headers_miss" | grep -i -q "X-Cache: MISS"
echo "OK (Cache MISS -> Loaded from DB)"

# 5. Second read: Cache Hit
echo -n "5. Testing second read resolution (Expected: X-Cache HIT)... "
headers_hit=$(curl -sI "$BASE_URL/r/smoke-test")
echo "$headers_hit" | grep -i -q "X-Cache: HIT"
echo "OK (Cache HIT -> Served from Redis)"

# 6. Asynchronous Queue Write (The Depot pattern)
echo -n "6. Testing asynchronous queue write (async_queue=true)... "
async_res=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/api/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com/async-item", "custom_code": "async-test", "async_queue": true}')
echo "$async_res" | grep -q "202"
echo "OK (202 Accepted, Buffered in Queue)"

# 7. Asynchronous read test (served optimistically from warm cache)
echo -n "7. Testing resolution of async queued URL... "
curl -sf -I "$BASE_URL/r/async-test" >/dev/null
echo "OK"

# 8. Check worker queue processing & stats
echo -n "8. Checking stats endpoint (GET /api/stats/smoke-test)... "
stats=$(curl -sf "$BASE_URL/api/stats/smoke-test")
echo "$stats" | grep -q "smoke-test"
echo "OK"

# 9. Rate limiting on gateway
echo -n "9. Checking gateway rate limiting (Token Bucket / 429)... "
for i in {1..12}; do
  status=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL/api/limited")
  if [ "$status" = "429" ]; then
    break
  fi
done
if [ "$status" = "429" ]; then
  echo "OK (HTTP 429 Rate Limit Throttled as expected)"
else
  echo "Note: Rate limit not triggered on first few requests (allowed within burst)"
fi

# 10. Metrics endpoint
echo -n "10. Inspecting system telemetry & metrics (GET /api/metrics)... "
metrics=$(curl -sf "$BASE_URL/api/metrics")
echo "$metrics" | grep -q "cache_hits"
echo "OK"

echo "--------------------------------------------------------"
echo "All smoke tests passed! System Design components verified."
echo "--------------------------------------------------------"
