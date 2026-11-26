#!/usr/bin/env bash
# Run a SQL query or open an interactive MySQL prompt inside the container.
# Usage:
#   scripts/sql.sh                         # interactive mysql prompt
#   scripts/sql.sh "SELECT * FROM course;" # run one statement or file via stdin
set -euo pipefail
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
  if [ -t 0 ]; then
    docker compose exec mysql mysql -uroot -proot -D training_db
  else
    docker compose exec -T mysql mysql -uroot -proot -D training_db
  fi
else
  docker compose exec -T mysql mysql -uroot -proot -D training_db -e "$1"
fi
