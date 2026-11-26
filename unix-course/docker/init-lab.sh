#!/usr/bin/env bash
# Deterministic workspace seeder for /workspace/training_lab inside wbl-unix.
# Safe & idempotent on restart; pass --force to wipe and re-seed from scratch.
set -euo pipefail

BASE="/workspace/training_lab"

if [ "${1:-}" = "--force" ]; then
  rm -rf "${BASE:?}/docs" "${BASE:?}/logs" "${BASE:?}/bin" "${BASE:?}/config" "${BASE:?}/tmp" "${BASE:?}/archive" "${BASE:?}/.seeded"
fi

if [ -f "${BASE}/.seeded" ]; then
  exit 0
fi

mkdir -p "${BASE}/docs" "${BASE}/logs" "${BASE}/bin" "${BASE}/config" "${BASE}/tmp" "${BASE}/archive"

# 1. docs/ (Case sensitivity + relative/absolute path navigation + servers CSV)
cat > "${BASE}/docs/readme.txt" <<'EOF'
Whitebox Learning — Unix & Shell Scripting Lab
Workspace: /workspace/training_lab
All modules run against deterministic files inside this tree.
Start with: pwd, ls -la, cat docs/readme.txt
Do not guess outputs — verify line and file counts.
EOF

cat > "${BASE}/docs/Report.txt" <<'EOF'
Quarterly Summary (Uppercase Report.txt)
Status: FINAL
Owner: devuser
Note: Unix filenames are case-sensitive!
EOF

cat > "${BASE}/docs/report.txt" <<'EOF'
Daily Draft (Lowercase report.txt)
Status: DRAFT
Owner: root
Note: This is a completely separate file from Report.txt.
EOF

cat > "${BASE}/docs/servers.csv" <<'EOF'
host,region,role,cpu_pct,status
web-01,us-east,web,34,healthy
web-02,us-east,web,78,healthy
api-01,us-west,api,91,degraded
api-02,us-west,api,42,healthy
db-01,us-east,database,65,healthy
cache-01,eu-west,redis,22,healthy
worker-01,us-west,batch,96,critical
EOF

# 2. logs/app.log (Exactly 120 lines: 75 INFO, 25 WARN, 15 ERROR, 5 FATAL)
: > "${BASE}/logs/app.log"
for i in $(seq -w 1 75); do
  echo "2025-03-01 08:00:${i:0:2} INFO service=api req_id=10${i} status=200 latency_ms=$((12 + (10#$i % 30)))" >> "${BASE}/logs/app.log"
done
for i in $(seq -w 1 25); do
  echo "2025-03-01 08:05:${i:0:2} WARN service=worker req_id=20${i} msg=retrying_slow_downstream" >> "${BASE}/logs/app.log"
done
for i in $(seq -w 1 15); do
  echo "2025-03-01 08:10:${i:0:2} ERROR service=auth user_id=$((100 + 10#$i)) msg=token_validation_failed" >> "${BASE}/logs/app.log"
done
for i in $(seq -w 1 5); do
  echo "2025-03-01 08:15:${i:0:2} FATAL service=db code=ECONNREFUSED msg=primary_pool_exhausted" >> "${BASE}/logs/app.log"
done

# 3. logs/auth.log (Exactly 30 lines: 22 Accepted, 8 Failed password)
: > "${BASE}/logs/auth.log"
for i in $(seq 1 22); do
  echo "Mar 01 09:00:$(printf '%02d' "$i") wbl-unix sshd[10${i}]: Accepted publickey for devuser from 10.0.1.$((i + 10)) port 51${i} ssh2" >> "${BASE}/logs/auth.log"
done
for i in $(seq 1 8); do
  ip_last=$(( (i % 2) + 50 ))
  echo "Mar 01 09:05:$(printf '%02d' "$i") wbl-unix sshd[20${i}]: Failed password for invalid user admin from 192.168.99.${ip_last} port 44${i} ssh2" >> "${BASE}/logs/auth.log"
done

# 4. bin/ scripts (Module 2 chmod lab & Module 4 bash lab)
cat > "${BASE}/bin/healthcheck.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
echo "HOST=$(hostname) USER=$(whoami) TIME=$(date -u +%H:%M:%S)"
exit 0
EOF
chmod 755 "${BASE}/bin/healthcheck.sh"

cat > "${BASE}/bin/backup.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
TARGET_DIR="/workspace/training_lab/archive"
if [ ! -d "$TARGET_DIR" ]; then
  echo "ERROR: archive directory missing: $TARGET_DIR" >&2
  exit 2
fi
tar -czf "${TARGET_DIR}/config-backup.tar.gz" -C /workspace/training_lab config >/dev/null 2>&1
echo "OK: backed up config to ${TARGET_DIR}/config-backup.tar.gz"
exit 0
EOF
chmod 755 "${BASE}/bin/backup.sh"

cat > "${BASE}/bin/onboarding_helper.sh" <<'EOF'
#!/usr/bin/env bash
# Deliberately lacks +x permission at start for Module 2 chmod demo
echo "Welcome to WBL Unix Workshop, $(whoami)!"
EOF
chmod 644 "${BASE}/bin/onboarding_helper.sh"

# 5. config/
cat > "${BASE}/config/app.conf" <<'EOF'
APP_NAME=wbl-portal
ENV=training
PORT=8080
LOG_LEVEL=INFO
MAX_WORKERS=4
RETRY_LIMIT=3
EOF

cat > "${BASE}/config/sshd_config.sample" <<'EOF'
# Hardened SSH Server Reference (Slide 42)
Port 22
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
AllowUsers devuser
EOF

chown -R root:root "${BASE}"
chmod -R a+rX "${BASE}"
# Ensure onboarding_helper.sh stays 644 (not executable)
chmod 644 "${BASE}/bin/onboarding_helper.sh"

touch "${BASE}/.seeded"
echo "Seeded /workspace/training_lab cleanly."
