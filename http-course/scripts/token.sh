#!/usr/bin/env bash
# Print an access token for a demo user. Usage: HR=$(scripts/token.sh hr_admin)
# Users: hr_admin, manager, employee.  Password comes from the running API's environment.
set -e
cd "$(dirname "$0")/.."
user="${1:?usage: scripts/token.sh hr_admin|manager|employee}"
pw=$(docker compose exec -T api printenv DEMO_PASSWORD)
curl -sf -X POST "${BASE:-http://localhost:8000}/v2/auth/token" -d "username=$user" --data-urlencode "password=$pw" \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"
