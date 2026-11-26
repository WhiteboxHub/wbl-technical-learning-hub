# Workspace Lab Reference (`/workspace/training_lab` — Deterministic Counts)

Use this reference to **predict expected counts and outputs** before running commands (`Prediction Rule`). Every count below is seeded deterministically by `docker/init-lab.sh`.

---

## 1. Directory Tree (`wbl-unix` Container, Ubuntu 24.04)
```text
/workspace/training_lab/
├── docs/
│   ├── readme.txt              # 5 lines
│   ├── Report.txt              # 4 lines (Uppercase R — Status: FINAL, Owner: devuser)
│   ├── report.txt              # 4 lines (Lowercase r — Status: DRAFT, Owner: root)
│   └── servers.csv             # 8 lines (1 header + 7 hosts)
├── logs/
│   ├── app.log                 # 120 lines (75 INFO, 25 WARN, 15 ERROR, 5 FATAL)
│   └── auth.log                # 30 lines  (22 Accepted publickey, 8 Failed password)
├── bin/
│   ├── healthcheck.sh          # 755 (executable), exits 0
│   ├── backup.sh               # 755 (executable), archives config/ -> archive/config-backup.tar.gz
│   └── onboarding_helper.sh    # 644 (NOT executable at start — triggers Permission denied for devuser)
├── config/
│   ├── app.conf                # 6 lines (APP_NAME, ENV, PORT=8080, LOG_LEVEL, MAX_WORKERS, RETRY_LIMIT)
│   └── sshd_config.sample      # 6 lines (Port 22, PermitRootLogin no, PasswordAuthentication no, ...)
├── archive/                    # empty at start (target for backup.sh)
└── tmp/                        # empty at start (scratch folder for lab & fault demos)
```

---

## 2. Exact Seed Counts & Known Facts

| Item / Check | Exact Value | Notes |
|---|---|---|
| Non-root user | `devuser` (UID `1000`, `/home/devuser`) | Also `root` (UID `0`) exists |
| Case-sensitive pair in `docs/` | `2` files (`Report.txt`, `report.txt`) | Distinct files with different contents |
| `docs/servers.csv` lines | `8` total (`7` data rows) | Hosts with `status != healthy`: **`2`** (`api-01` degraded 91%, `worker-01` critical 96%); hosts with `cpu_pct >= 75`: **`3`** (`web-02` 78%, `api-01` 91%, `worker-01` 96%) |
| `logs/app.log` total lines | `120` | `75` `INFO` + `25` `WARN` + `15` `ERROR` + `5` `FATAL` |
| `grep -cE 'ERROR\|FATAL' logs/app.log` | `20` | `15` + `5` |
| `logs/auth.log` total lines | `30` | `22` `Accepted publickey` + `8` `Failed password` |
| Failing IPs in `logs/auth.log` | `192.168.99.50` (`4` hits), `192.168.99.51` (`4` hits) | Ideal for `grep \| awk \| sort \| uniq -c` |
| Listening TCP service inside container | Port `8080` (`python3 -m http.server`) | Mapped to host port `8085` |

---

## 3. Injected Faults (`scripts/break.sh <fault>`)
- `bad-perms`: sets `bin/backup.sh` to `644` (`Permission denied` on direct execution).
- `runaway-proc`: launches a persistent background sleep loop tagged `wbl_runaway_worker`.
- `disk-bloat`: writes a `12 MB` file `/workspace/training_lab/tmp/huge_debug.dump`.
- `missing-archive`: hides `/workspace/training_lab/archive` -> `bin/backup.sh` exits `2`.
- `broken-cron-script`: writes `/workspace/training_lab/bin/nightly_job.sh` with `\r\n` CRLF (`^M: bad interpreter`).
- `stale-lockfile`: creates `/workspace/training_lab/tmp/deploy.lock` with non-existent PID `99999`.

Run `scripts/fix.sh` anytime to restore the clean baseline.
