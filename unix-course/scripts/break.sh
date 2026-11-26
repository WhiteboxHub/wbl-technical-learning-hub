#!/usr/bin/env bash
# Live fault injector (Module 4). Usage: scripts/break.sh <fault>   Undo: scripts/fix.sh
# Faults: bad-perms | runaway-proc | disk-bloat | missing-archive | broken-cron-script | stale-lockfile
# The instructor runs this; candidates diagnose with ls -l, ps aux, du -sh, grep, and exit codes ($?) before fixing.
set -e
cd "$(dirname "$0")/.."

in_unix() {
  docker compose exec -T unix bash -lc "$1"
}

case "${1:-}" in
  bad-perms)
    in_unix "chmod 644 /workspace/training_lab/bin/backup.sh"
    echo "fault injected: bad-perms (try running: scripts/sh.sh \"./bin/backup.sh\")"
    ;;
  runaway-proc)
    docker compose exec -d unix bash -c 'while true; do sleep 5; done # wbl_runaway_worker'
    echo "fault injected: runaway-proc (find it with: scripts/sh.sh \"ps aux | grep wbl_runaway_worker\")"
    ;;
  disk-bloat)
    in_unix "dd if=/dev/zero of=/workspace/training_lab/tmp/huge_debug.dump bs=1M count=12 status=none"
    echo "fault injected: disk-bloat (inspect with: scripts/sh.sh \"du -sh /workspace/training_lab/*\")"
    ;;
  missing-archive)
    in_unix "if [ -d /workspace/training_lab/archive ]; then mv /workspace/training_lab/archive /workspace/training_lab/.archive.bak; fi"
    echo "fault injected: missing-archive (try running: scripts/sh.sh \"./bin/backup.sh\")"
    ;;
  broken-cron-script)
    in_unix "printf '#!/bin/bash\r\necho running\r\nexit 0\r\n' > /workspace/training_lab/bin/nightly_job.sh && chmod 755 /workspace/training_lab/bin/nightly_job.sh"
    echo "fault injected: broken-cron-script (CRLF script fails with bad interpreter; run: scripts/sh.sh \"./bin/nightly_job.sh\")"
    ;;
  stale-lockfile)
    in_unix "echo 99999 > /workspace/training_lab/tmp/deploy.lock"
    echo "fault injected: stale-lockfile (PID 99999 in /workspace/training_lab/tmp/deploy.lock does not exist in ps aux)"
    ;;
  *)
    echo "usage: scripts/break.sh bad-perms|runaway-proc|disk-bloat|missing-archive|broken-cron-script|stale-lockfile"
    exit 1
    ;;
esac
