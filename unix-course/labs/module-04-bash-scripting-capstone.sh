#!/usr/bin/env bash
# Module 4 Lab: Bash Scripting, Exit Codes, Fault Triage & Post-Class Capstone

# 1. Write `/workspace/training_lab/tmp/log_guard.sh` with `#!/usr/bin/env bash` and `set -euo pipefail`:
#    - Accept log file path as `$1` (or prompt with `read -r -p` if omitted)
#    - Count `ERROR` lines (`grep -c "ERROR" "$LOG_FILE" || true`)
#    - Exit `2` if > 10 ("CRITICAL"), `1` if > 0 ("WARN"), `0` if 0 ("OK")
#    - Test both `logs/app.log` (Expected exit 2, 15 errors) and `logs/auth.log` (Expected exit 0) and inspect `echo $?`!


# 2. Test short-circuit error handling (`&&` and `||`) using `./bin/healthcheck.sh` and a failing `ls` command:


# 3. Post-Class Capstone Script (`/workspace/training_lab/tmp/triage_report.sh`):
#    a) Verify `docs/servers.csv` exists (`|| exit 1`).
#    b) Print all servers with `cpu_pct >= 80` (Expected: api-01 at 91%, worker-01 at 96%).
#    c) Print ranked count of `Failed password` source IPs from `logs/auth.log`.
#    d) Check `du -sm tmp` is `< 50` MB; if safe, run `./bin/backup.sh`. Clean up `tmp/*.sh` afterwards.
