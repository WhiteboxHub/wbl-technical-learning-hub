# Self-Study 3 — Backend/DevOps Linux, 12 Production Scenarios & Interview Bank (Levels 9–10)

> **For Candidates & AI Agents:** Study this **after** Self-Study 1 & 2 to connect daily Linux administration directly to backend deployment, Reverse Proxies, Docker internals, the 12 classic production failure scenarios, and tiered technical interviews.

---

### D1 — Linux for Backend Developers & DevOps (Level 9)
1. **Service User Isolation & Ownership:** Run your API under a dedicated non-root user (e.g., `appuser` or `devuser`), `chown -R appuser:appuser /opt/myapp`, and store configs read-only (`640`/`600`) so a compromised web worker cannot overwrite system files.
2. **Environment Configuration & Secrets:** Pass DB URLs / API keys via environment files (`chmod 600 .env` or `systemd` `EnvironmentFile=`) — **never commit `.env` or secrets to Git**, and never echo secret env vars into logs.
3. **Reverse Proxy Pattern (Nginx -> App on `127.0.0.1`):**
   - Your Python/Node API listens on **`127.0.0.1:8000`** (internal only), managed by `systemd`.
   - **Nginx** binds **`0.0.0.0:80` / `443`**, handles TLS + static files, and forwards via `proxy_pass http://127.0.0.1:8000;`.
   - Contrast with a **containerized app** in Docker: inside a container, the app MUST bind **`0.0.0.0:8000`**, otherwise Docker port publishing (`-p 8080:8000`) cannot reach `127.0.0.1` across the container network namespace!
4. **Why Docker Needs Linux (Namespaces & Cgroups):**
   - Containers are **not** virtual machines — they share the host Linux kernel!
   - **Namespaces** isolate what a process *sees* (`PID`, network interfaces/`ss`, filesystem mounts, hostname).
   - **cgroups (Control Groups)** limit what a process *uses* (CPU shares, RAM limit -> `OOMKilled` exit code `137`).

---

### D2 — 12 Production Troubleshooting Scenarios (Level 10 Diagnostic Matrix)

Use this table for **Scenario Drills** with your Practice Agent / Quiz Agent (investigate with read-only commands first -> identify root cause -> apply safe fix):

| # | Incident Symptom | First 2 Diagnostic Commands | Common Root Cause | Safe Fix & Verify |
|---|---|---|---|---|
| **1** | App is not responding | `systemctl status app` ; `curl -i localhost:<port>` | Process crashed, hung, or blocked on downstream DB | Inspect `journalctl -u app -n 50`; fix cause; `sudo systemctl restart app` |
| **2** | App cannot bind to port (`Address already in use` / `Permission denied`) | `sudo ss -tulpn \| grep :<port>` | Another PID already holds `<port>`, or non-root user tried privileged port `< 1024` | Stop conflicting process OR listen on port `>= 1024` behind Nginx `:80/443` |
| **3** | Disk space exhausted (`No space left`) | `df -h && df -i` ; `du -sh /* 2>/dev/null \| sort -h` | Giant logs/dumps OR 100% inode exhaustion OR deleted open file (`lsof +L1`) | Truncate/rotate safely, delete old dumps, or reload service holding deleted FD |
| **4** | App permission errors | `ps aux \| grep app` ; `ls -ld <path>` | App runs as `devuser` while files are owned by `root` (`600`) or script lacks `+x` | `sudo chown appuser:appuser ...` or `chmod 750`/`640` (never `777`!) |
| **5** | Process consuming 100% CPU | `top` (or `ps aux --sort=-%cpu \| head`) ; `strace`/logs | Tight infinite loop, unindexed query spike, or runaway worker | Inspect thread/logs, throttle (`renice`) or terminate cleanly (`kill` -> `-9` last resort) |
| **6** | Process consuming excessive memory / OOM | `free -h` ; `dmesg -T \| grep -i oom` ; `ps aux --sort=-%mem` | Memory leak, unbounded cache/batch load, or missing cgroup/swap headroom | Restart/cap workers, tune batch size/cache TTL, inspect `journalctl` for OOM `137` |
| **7** | SSH connection failing | `ssh -vvv user@host` ; `grep Failed /var/log/auth.log` | Wrong key/bad perms (`666`), wrong username/port, firewall/SG blocking `:22` | Fix `chmod 700 ~/.ssh && chmod 600 ~/.ssh/id_*`, allow `:22`, inspect `sshd_config` |
| **8** | DNS resolution failing | `dig example.com` / `nslookup ...` ; `cat /etc/resolv.conf` | Bad/unreachable DNS resolver in `/etc/resolv.conf` or typo in `/etc/hosts` | Compare IP `ping` vs hostname `ping`, fix `/etc/resolv.conf` / DNS settings |
| **9** | Logs show repeated errors | `grep -cE "ERROR\|FATAL" app.log` ; `tail -n 30 app.log` | Upstream timeout, bad DB credentials, expired TLS cert or token | Extract unique error messages (`sort \| uniq -c`), fix upstream/config |
| **10** | Service fails after reboot | `systemctl is-enabled app` ; `journalctl -b -u app` | Unit was `started` manually but never `enabled`, or `/etc/fstab`/env not ready | `sudo systemctl enable app` + verify `After=network-online.target` |
| **11** | Bash script exits unexpectedly | `bash -x ./script.sh` ; check `set -e` / `head -n 1 \| cat -A` | Failing command under `set -e`, unset var under `-u`, or `\r` CRLF (`^M`) | Trace with `bash -x`, strip `\r` via `sed -i 's/\r$//'`, handle optional errors with `\|\| true` |
| **12** | Deployment fails on env config | Compare `printenv` / `.env` vs `systemctl show app` | Missing env var, quoted literal bug, or non-interactive shell skipping `~/.bashrc` | Put shared vars in systemd `EnvironmentFile=` or `.env`, never `~/.bashrc` |

---

### D3 — Graded Practice Drills & Tiered Interview Question Bank

#### Practice Labs (Isolated in `wbl-unix` Container — Never Break Your Host!)
- **Beginner:** `labs/module-01-architecture-paths-nav.sh` & `labs/module-02-permissions-grep-pipes.sh` (navigation, case sensitivity, `chmod`, `grep -cE`).
- **Intermediate:** `labs/module-03-processes-networking-security.sh` & `labs/module-04-bash-scripting-capstone.sh` (`ps`/`kill`, `ss -tuln`, threshold & `servers.csv` audit Bash scripts).
- **Advanced (Live Fault Triage):** Run all 6 faults in `scripts/break.sh` (`bad-perms`, `runaway-proc`, `disk-bloat`, `missing-archive`, `broken-cron-script`, `stale-lockfile`), diagnose with read-only commands first, write the exact fix + verification output, and explain why each happened before running `scripts/fix.sh`.

#### Interview Question Bank (Ask Your Quiz Agent to Test by Level)
- **Beginner:**
  1. Difference between Kernel and Shell? Relative vs Absolute path?
  2. Convert `-rwxr-x---` to octal, and explain why `chmod 777` is dangerous.
  3. Find all lines containing `ERROR` case-insensitively with line numbers in `app.log`.
- **Intermediate:**
  4. Why try `kill <PID>` before `kill -9 <PID>`? Can `kill -9` kill a Zombie (`Z`) process?
  5. Difference between binding `127.0.0.1:8080` vs `0.0.0.0:8080` (especially in Nginx vs Docker)?
  6. Why does `cat access.log | uniq -c` fail to count total IPs unless `sort` runs first?
  7. Write a Bash script snippet using `set -euo pipefail`, `if [ ... -gt ... ]`, and `exit 1`.
- **Senior / Backend & DevOps:**
  8. A server reports `"No space left on device"` while `df -h` shows 40% free — name two causes (`df -i` inode exhaustion, or deleted file still held open by a running process via `lsof +L1`).
  9. Contrast Hard Links (`ln`) vs Symbolic Links (`ln -s`) and explain how `/tmp` (`1777`) Sticky Bit protects users.
  10. A script passes interactively (`./backup.sh`) but fails silently inside `crontab` — list 3 reasons why.
  11. Explain how Docker containers achieve isolation on a shared Linux kernel (Namespaces vs cgroups + exit code `137`).
