#!/usr/bin/env bash
# Capstone fault injector (Module 8). Usage: scripts/break.sh <fault>     Undo everything: scripts/fix.sh
# Faults: expired-token | wrong-role | missing-cors | rate-limit | departments-down | stale-cache
# The instructor runs this; candidates diagnose from evidence (status codes, headers, logs) before anyone fixes it.
set -e
cd "$(dirname "$0")/.."
F="-f docker-compose.yml -f docker-compose.cors.yml"
wait_api() { for _ in $(seq 1 30); do curl -sf http://localhost:8000/health >/dev/null && return; sleep 1; done; }
case "${1:-}" in
  expired-token)      # tokens now live 5 seconds
    TOKEN_TTL=5 docker compose $F -f docker-compose.auth.yml up -d api >/dev/null 2>&1; wait_api
    echo "fault injected: expired-token" ;;
  wrong-role)         # auth on, normal lifetime: a manager asking for another department's salary
    TOKEN_TTL=900 docker compose $F -f docker-compose.auth.yml up -d api >/dev/null 2>&1; wait_api
    echo "fault injected: wrong-role" ;;
  missing-cors)       # the web page can no longer read the API
    docker compose -f docker-compose.yml up -d api >/dev/null 2>&1; wait_api
    echo "fault injected: missing-cors" ;;
  rate-limit)         # gateway limits every route to a trickle
    sed 's#    location / {#    location / {\n        limit_req zone=demo burst=1 nodelay;#' gateway/nginx.conf > gateway/.fault.conf
    printf 'services:\n  gateway:\n    volumes:\n      - ./gateway/.fault.conf:/etc/nginx/conf.d/default.conf:ro\n' > .fault-override.yml
    docker compose $F -f .fault-override.yml up -d --force-recreate gateway >/dev/null 2>&1
    echo "fault injected: rate-limit" ;;
  departments-down)   # needs the split stack; the dependency hangs (not refuses)
    docker compose -f docker-compose.yml -f docker-compose.split.yml up -d >/dev/null 2>&1
    docker compose -f docker-compose.yml -f docker-compose.split.yml pause departments-service >/dev/null
    echo "fault injected: departments-down" ;;
  stale-cache)        # a wrong departments list is sitting in Redis for an hour
    docker compose exec -T redis redis-cli SET departments:list '[{"id":1,"name":"Human Resources","location":"Pleasanton"},{"id":2,"name":"Engineering","location":"Old Office"}]' EX 3600 >/dev/null
    echo "fault injected: stale-cache" ;;
  *) echo "usage: scripts/break.sh expired-token|wrong-role|missing-cors|rate-limit|departments-down|stale-cache"; exit 1 ;;
esac
