#!/usr/bin/env bash
# Smoke test for the MySQL Training Management DB stack. Usage: scripts/smoke.sh
set -u
cd "$(dirname "$0")/.."

fail=0

sql_val() {
  docker compose exec -T mysql mysql -N -uroot -proot -D training_db -e "$1" 2>/dev/null | tr -d '\r' | tail -n 1
}

check_eq() {
  local label="$1" want="$2" query="$3" got
  got=$(sql_val "$query")
  if [ "$got" = "$want" ]; then
    echo "PASS  $label ($got)"
  else
    echo "FAIL  $label: wanted '$want', got '$got'"
    fail=1
  fi
}

check_eq "mysql version 8.x"           "8"    "SELECT LEFT(VERSION(), 1);"
check_eq "instructor seed count"       "3"    "SELECT COUNT(*) FROM instructor;"
check_eq "course seed count"           "6"    "SELECT COUNT(*) FROM course;"
check_eq "subject seed count"          "5"    "SELECT COUNT(*) FROM subject;"
check_eq "student seed count"          "8"    "SELECT COUNT(*) FROM student;"
check_eq "enrollment seed count"       "12"   "SELECT COUNT(*) FROM enrollment;"
check_eq "trigger populated log count" "12"   "SELECT COUNT(*) FROM enrollment_log;"
check_eq "activity_log seed count"     "2000" "SELECT COUNT(*) FROM activity_log;"
check_eq "LEFT JOIN unmatched students" "2"   "SELECT COUNT(*) FROM student s LEFT JOIN enrollment e ON s.id = e.student_id WHERE e.id IS NULL;"
check_eq "NULL phone count"            "2"    "SELECT COUNT(*) FROM student WHERE phone IS NULL;"
check_eq "normalized users count"      "2"    "SELECT COUNT(*) FROM users;"
check_eq "normalized contact_info"     "3"    "SELECT COUNT(*) FROM contact_info;"

# Verify Adminer web UI
code=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8082/ 2>/dev/null || echo 000)
if [ "$code" = "200" ]; then
  echo "PASS  Adminer web UI ($code)"
else
  echo "FAIL  Adminer web UI: wanted 200, got $code"
  fail=1
fi

# Verify Redis
pong=$(docker compose exec -T redis redis-cli PING 2>/dev/null | tr -d '\r')
if [ "$pong" = "PONG" ]; then
  echo "PASS  Redis cache ($pong)"
else
  echo "FAIL  Redis cache: wanted PONG, got '$pong'"
  fail=1
fi

echo
if [ "$fail" -eq 0 ]; then
  echo "ALL CHECKS PASSED"
else
  echo "SOME CHECKS FAILED"
  exit 1
fi
