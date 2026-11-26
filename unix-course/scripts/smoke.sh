#!/usr/bin/env bash
# Smoke test for the WBL Unix & Shell Scripting Lab container. Usage: scripts/smoke.sh
set -u
cd "$(dirname "$0")/.."

fail=0

in_unix() {
  docker compose exec -T unix bash -lc "$1" 2>/dev/null | tr -d '\r' | tail -n 1
}

check_eq() {
  local label="$1" want="$2" cmd="$3" got
  got=$(in_unix "$cmd")
  if [ "$got" = "$want" ]; then
    echo "PASS  $label ($got)"
  else
    echo "FAIL  $label: wanted '$want', got '$got'"
    fail=1
  fi
}

check_eq "OS is Linux"                "Linux"  "uname -s"
check_eq "devuser exists"             "devuser" "id -un devuser"
check_eq "docs/servers.csv line count" "8"     "wc -l < /workspace/training_lab/docs/servers.csv"
check_eq "case-sensitive two reports" "2"      "ls -1 /workspace/training_lab/docs/*eport.txt | wc -l"
check_eq "logs/app.log total lines"   "120"    "wc -l < /workspace/training_lab/logs/app.log"
check_eq "logs/app.log ERROR count"   "15"     "grep -c 'ERROR' /workspace/training_lab/logs/app.log"
check_eq "logs/app.log FATAL count"   "5"      "grep -c 'FATAL' /workspace/training_lab/logs/app.log"
check_eq "logs/auth.log total lines"  "30"     "wc -l < /workspace/training_lab/logs/auth.log"
check_eq "logs/auth.log Failed count" "8"      "grep -c 'Failed password' /workspace/training_lab/logs/auth.log"
check_eq "backup.sh is executable"    "yes"    "test -x /workspace/training_lab/bin/backup.sh && echo yes || echo no"
check_eq "onboarding_helper lacks +x" "no"     "test -x /workspace/training_lab/bin/onboarding_helper.sh && echo yes || echo no"

# Verify HTTP port 8085 (docs listener inside container for network/curl demos)
code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8085/readme.txt 2>/dev/null || echo 000)
if [ "$code" = "200" ]; then
  echo "PASS  Lab HTTP service on :8085 ($code)"
else
  echo "FAIL  Lab HTTP service on :8085: wanted 200, got $code"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED"
  exit 1
fi
