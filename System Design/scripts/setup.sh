#!/usr/bin/env bash
# Setup and management script for System Design Course Stack
set -e
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$DIR"

stop_stack() {
  echo "Stopping System Design stack..."
  docker compose -f docker-compose.yml -f docker-compose.scale.yml down -v --remove-orphans >/dev/null 2>&1 || true
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
  echo "Stack stopped."
}

reset_stack() {
  echo "Resetting stack to clean seed state..."
  docker compose down -v --remove-orphans >/dev/null 2>&1 || true
  docker compose up --build -d
  wait_for_health
  "$DIR/scripts/smoke.sh"
}

wait_for_health() {
  echo "Waiting for API to be healthy at http://localhost:8000/health..."
  for i in $(seq 1 30); do
    if curl -sf http://localhost:8000/health >/dev/null 2>&1; then
      echo "API is healthy!"
      return 0
    fi
    sleep 1
  done
  echo "Error: API did not become healthy in time."
  docker compose logs
  exit 13
}

case "${1:-}" in
  --stop)
    stop_stack
    exit 0
    ;;
  --reset)
    reset_stack
    exit 0
    ;;
  --scale)
    echo "Starting stack in SCALED (3 replicas behind Load Balancer) mode..."
    docker compose -f docker-compose.yml -f docker-compose.scale.yml up --build -d
    wait_for_health
    "$DIR/scripts/smoke.sh"
    exit 0
    ;;
  --nocache)
    echo "Starting stack with NO CACHE to simulate database bottleneck..."
    docker compose -f docker-compose.yml -f docker-compose.nocache.yml up --build -d
    wait_for_health
    "$DIR/scripts/smoke.sh"
    exit 0
    ;;
esac

echo "=========================================================="
echo " Starting System Design Stack: The Growing City Demo"
echo "=========================================================="

# Check Docker daemon
if ! docker info >/dev/null 2>&1; then
  echo "Error: Docker Desktop is not running. Please start Docker."
  exit 11
fi

docker compose up --build -d
wait_for_health
"$DIR/scripts/smoke.sh"

echo ""
echo "=========================================================="
echo " [READY] System Design Stack is fully operational!"
echo " - Gateway / Load Balancer: http://localhost:8080"
echo " - Direct App Node:        http://localhost:8000"
echo " - Redis Cache & Queues:   localhost:6379"
echo " - Health Endpoint:        http://localhost:8080/health"
echo " - System Metrics:         http://localhost:8080/api/metrics"
echo "=========================================================="
