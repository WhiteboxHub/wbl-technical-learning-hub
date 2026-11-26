# Instructor Guide — 2-Hour Unix & Shell Scripting Class

Teach Unix Architecture, Permissions, `grep`/Pipes, Processes, Networking & Bash Scripting cleanly inside a **2-hour (120-minute)** live session using an AI co-pilot and the shared **Ubuntu 24.04 Unix Lab** (`/workspace/training_lab`).

**In a hurry? See the [Class-Day Quick Start](class-day-quickstart.md).**

---

## 1. How the 2-Hour Class Works
- **You teach; the agent keeps the 120-minute clock.** It runs live shell demos via `scripts/sh.sh`, surfaces plain-English **Candidate Takeaways**, and holds quiz answers until you ask.
- **Why only 4 Modules?** Low-ROI topics (long PDP-7 history, `mount`/`umount` hardware drills, writing deep `awk`/PAM configs or `cron` jobs live) were cut or moved to `course/self-study/` so you finish every high-signal topic in **120 minutes** without rushing.
- **The Storytelling Rule:** *Tell them what you are going to tell them -> Tell them -> Tell them what you told them* using each module's Story Anchor.

| # | Module | 2-Hr Budget | Story Anchor |
|---|---|---|---|
| 1 | Unix Architecture, Directory Tree & Paths | **25 min** | The Time-Travelling Workshop (Map & Spoken Orders) |
| 2 | Permissions, `grep` & Unix Pipes | **35 min** | The Workshop Badges & The Log Magnifying Glass |
| 3 | Processes, Networking, Packages & Security | **30 min** | The Running Assembly Line & The Network Gates |
| 4 | Bash Scripting, Exit Codes & Live Fault Triage | **30 min** | The Repeatable Recipe Card & The Incident Shift |

---

## 2. Before Class (One Time)
1. Install **Docker Desktop** and an AI coding agent (**Claude Code**, **Antigravity**, or **Cursor**).
2. Open `wbl-technical-learning-hub/unix-course` in a **new session**.
3. Say **"set up the class"** (`setup-unix-class`). Wait for **READY**.
4. Say **"teach class"** (or **"teach module 1"** … **"teach module 4"**).

**If running behind during class:** skip the second demo or second `Ask` question in Beats 1.2, 3.3, or 4.1. Never skip **Beat 2.1 (`chmod`)**, **Beat 2.2–2.3 (`grep` & Pipes)**, **Beat 3.1 (`ps`/`kill`)**, or **Beat 4.2–4.3 (Exit codes `$?` + live faults)**.

---

## 3. Known Facts About `/workspace/training_lab`
- **Docs:** `docs/Report.txt` != `docs/report.txt` (case sensitivity), `docs/servers.csv` (`8` lines; `2` non-healthy hosts: `api-01`, `worker-01`).
- **Logs:** `logs/app.log` has **120 lines** (`75 INFO`, `25 WARN`, `15 ERROR`, `5 FATAL`); `logs/auth.log` has **30 lines** (`22 Accepted`, `8 Failed password` split 4+4 across `192.168.99.50` & `.51`).
- **Permissions:** `bin/onboarding_helper.sh` starts at `644` (`Permission denied` for `devuser`); `bin/backup.sh` and `bin/healthcheck.sh` start at `755`.
- `scripts/break.sh <fault>` supports `bad-perms`, `runaway-proc`, `disk-bloat`, `missing-archive`, `broken-cron-script`, `stale-lockfile`; `scripts/fix.sh` restores the clean baseline.

---

## 4. Candidate Self-Study Loop (After the 2-Hour Class)
Send candidates [docs/student-guide.md](student-guide.md) and [docs/learning-plan.md](learning-plan.md). They open the repo in **Claude Code / Antigravity** (using `practice-unix`) or paste it into **ChatGPT / Gemini** to:
1. Re-learn any Beat from `course/modules/01–04` with its Story Anchor and practice **explaining the Candidate Takeaway in their own words**
2. Complete the 4 hands-on labs in `labs/` (predicting line/file counts before running) and debug Bash scripts with the **4-Rung Hint Ladder**
3. Continue into `course/self-study/01–03` for deeper high-ROI Linux skills (`find`, `df -i` inodes, `free -h`, `awk`/`sed`, Hard vs Soft links, `umask`/SUID/Sticky bit, `systemd`/`journalctl`, `cron`, Nginx/Docker internals, 12 production scenarios, and Tiered Interview Q&As)
4. Take an 8-question end-of-module quiz and send you their **Daily Report**.
