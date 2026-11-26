#!/usr/bin/env bash
# Run a Unix command inside the wbl-unix container or open an interactive bash session.
# Usage:
#   scripts/sh.sh                       # interactive bash prompt in /workspace/training_lab
#   scripts/sh.sh "grep -c ERROR logs/app.log"
set -euo pipefail
cd "$(dirname "$0")/.."

if [ $# -eq 0 ]; then
  if [ -t 0 ]; then
    docker compose exec unix bash
  else
    docker compose exec -T unix bash
  fi
else
  docker compose exec -T unix bash -lc "$1"
fi
