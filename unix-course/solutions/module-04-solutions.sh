#!/usr/bin/env bash
# Module 4 Reference Solutions (Instructors & Post-Attempt Verification Only)
set -euo pipefail
cd /workspace/training_lab

# 1. Threshold check script
cat > /workspace/training_lab/tmp/check_threshold.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
threshold="${1:-}"
if [ -z "$threshold" ]; then
  read -r -p "Enter ERROR threshold: " threshold
fi
err_count=$(grep -c 'ERROR' /workspace/training_lab/logs/app.log)
if [ "$err_count" -gt "$threshold" ]; then
  echo "ALERT: $err_count errors exceed threshold ($threshold)"
  exit 1
else
  echo "OK: $err_count errors within threshold ($threshold)"
  exit 0
fi
EOF
chmod +x /workspace/training_lab/tmp/check_threshold.sh
/workspace/training_lab/tmp/check_threshold.sh 20
echo "Exit code (threshold=20): $?"
/workspace/training_lab/tmp/check_threshold.sh 10 || echo "Caught non-zero exit (threshold=10): $?"
rm -f /workspace/training_lab/tmp/check_threshold.sh

# 2. Short-circuit logic:
#    cmd1 && cmd2 -> run cmd2 ONLY if cmd1 exited 0 (success)
#    cmd1 || cmd2 -> run cmd2 ONLY if cmd1 exited non-zero (failure)

# 3. Post-Class Capstone: server_audit.sh
cat > /workspace/training_lab/tmp/server_audit.sh <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
FILE="/workspace/training_lab/docs/servers.csv"
unhealthy=$(awk -F',' 'NR > 1 && $5 != "healthy" { printf "%s (%s) status=%s cpu=%s%%\n", $1, $2, $5, $4 }' "$FILE")
if [ -n "$unhealthy" ]; then
  echo "=== UNHEALTHY SERVERS FOUND ==="
  echo "$unhealthy"
  exit 1
fi
echo "All servers healthy."
exit 0
EOF
chmod +x /workspace/training_lab/tmp/server_audit.sh
/workspace/training_lab/tmp/server_audit.sh || echo "Capstone exited 1 as expected (2 unhealthy hosts: api-01, worker-01)"
rm -f /workspace/training_lab/tmp/server_audit.sh
