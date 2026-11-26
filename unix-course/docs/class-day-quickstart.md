# Class-Day Quick Start (1-Page Cheat Sheet)

Run a **2-hour (120-minute)** live Unix class smoothly with zero setup drama.

## 1. Before Class (5 Minutes)
1. Start **Docker Desktop** (wait until status is running).
2. Open `wbl-technical-learning-hub/unix-course` in your AI coding agent (**Claude Code**, **Antigravity**, **Cursor**).
3. Type:
   ```text
   set up the class
   ```
   Wait until it prints **READY** (`wbl-unix` container up, `120` lines in `logs/app.log`, `:8085` -> `200`).

---

## 2. Live 2-Hour Flow
Type:
```text
teach class
```
*(Or `teach module 1` … `teach module 4` if teaching modules individually.)*

| Clock | Module | Time | Must-Hit Demos |
|---|---|---|---|
| `0:00–0:25` | **1** Architecture & Paths | 25m | `Report.txt` vs `report.txt`, `/etc/passwd`, relative `../config/app.conf` |
| `0:25–1:00` | **2** Permissions, `grep` & Pipes | 35m | `Permission denied` -> `chmod 755`, `grep -cE`, `grep \| awk \| sort \| uniq -c` |
| `1:00–1:30` | **3** Processes, Net & Security | 30m | `ps aux`, background `sleep` + `kill` (`SIGTERM`), `ss -tuln`, `sshd_config.sample` |
| `1:30–2:00` | **4** Bash Scripting & Faults | 30m | `#!/bin/bash` + `-gt` + `$?`, `&&`/`\|\|`, `scripts/break.sh bad-perms` & `runaway-proc` |

**Co-pilot keys while teaching:** `next` · `answer` · `skip` · `status` (checks 120-min pace!) · `jump N.M` · `end`

---

## 3. After Class Cleanup & Handoff
1. Reset any live demo faults:
   ```bash
   scripts/fix.sh
   ```
2. Send candidates [docs/student-guide.md](student-guide.md) and [docs/learning-plan.md](learning-plan.md) so they practice Modules 1–4, complete `labs/`, continue into `course/self-study/`, and email you their **Daily Report**.
3. Optional stop: `scripts/setup.sh --stop`.
