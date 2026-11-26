#!/usr/bin/env bash
# Module 3 Reference Solutions (Instructors & Post-Attempt Verification Only)
set -euo pipefail
cd /workspace/training_lab

# 1. Process inspection
ps aux | head -n 15

# 2. Job control + graceful SIGTERM termination
sleep 120 &
PID=$!
jobs -l
kill "$PID"
wait "$PID" 2>/dev/null || true

# 3. Network diagnostics
ip -br addr
ss -tuln || netstat -tuln
curl -sI http://localhost:8080/readme.txt

# 4. Security & SSH hardening (PermitRootLogin no + PasswordAuthentication no prevent root & brute-force logins)
id
id devuser
cat config/sshd_config.sample
