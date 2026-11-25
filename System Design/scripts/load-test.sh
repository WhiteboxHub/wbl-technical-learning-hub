#!/usr/bin/env bash
# Load testing script to demonstrate:
# 1. Latency difference between Cache HIT vs Cache MISS
# 2. Traffic distribution across multiple application replicas
set -e
URL="${1:-http://localhost:8080/r/wbl}"
REQUESTS="${2:-50}"

echo "=========================================================="
echo " Running System Design Load Test"
echo " Target: $URL"
echo " Total Requests: $REQUESTS"
echo "=========================================================="

echo "Sending $REQUESTS requests and measuring response headers..."

declare -A instances
hits=0
misses=0

for i in $(seq 1 "$REQUESTS"); do
  headers=$(curl -sI "$URL")
  instance=$(echo "$headers" | grep -i "X-Instance-Id" | awk -F': ' '{print $2}' | tr -d '\r')
  cache=$(echo "$headers" | grep -i "X-Cache" | awk -F': ' '{print $2}' | tr -d '\r')

  [ -n "$instance" ] && instances["$instance"]=$(( ${instances["$instance"]:-0} + 1 ))

  if [ "$cache" = "HIT" ]; then
    hits=$((hits + 1))
  else
    misses=$((misses + 1))
  fi
done

echo ""
echo "=== Test Results ==="
echo "Cache Hits:   $hits"
echo "Cache Misses: $misses"
echo ""
echo "Traffic Distribution by Instance ID (Load Balancing Proof):"
for inst in "${!instances[@]}"; do
  echo " - $inst: ${instances[$inst]} requests"
done
echo "=========================================================="
