#!/usr/bin/env bash
# Undo every injected Unix lab fault and restore the clean /workspace/training_lab baseline.
set -e
cd "$(dirname "$0")/.."

docker compose exec -T unix bash -lc '
  chmod 755 /workspace/training_lab/bin/backup.sh
  chmod 755 /workspace/training_lab/bin/healthcheck.sh
  chmod 644 /workspace/training_lab/bin/onboarding_helper.sh
  pkill -f "wbl_runaway_worker" >/dev/null 2>&1 || true
  rm -f /workspace/training_lab/tmp/huge_debug.dump \
        /workspace/training_lab/tmp/deploy.lock \
        /workspace/training_lab/bin/nightly_job.sh
  if [ -d /workspace/training_lab/.archive.bak ] && [ ! -d /workspace/training_lab/archive ]; then
    mv /workspace/training_lab/.archive.bak /workspace/training_lab/archive
  else
    mkdir -p /workspace/training_lab/archive
    rm -rf /workspace/training_lab/.archive.bak
  fi
'

echo "all faults cleared (permissions restored, runaway worker stopped, tmp/archive clean)"
