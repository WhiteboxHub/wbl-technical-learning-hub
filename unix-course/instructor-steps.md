# Instructor Steps: How to Start and Teach the 2-Hour Unix Class

Course: **Unix & Shell Scripting Essentials (2-Hour Live Class + AI Self-Study)**, taught with an AI co-pilot and a shared **Ubuntu 24.04 Unix Training Lab** (`/workspace/training_lab`).
Project folder: `unix-course/` (inside `wbl-technical-learning-hub`). More detail: [docs/instructor-guide.md](docs/instructor-guide.md) and [docs/class-day-quickstart.md](docs/class-day-quickstart.md).

## Before class
1. **Open the right folder.** Open `wbl-technical-learning-hub/unix-course` in Claude Code / Antigravity and start a **new session**.
2. **Start Docker Desktop** and wait until it says running.
3. **Open your slides** (`UNIX.pdf`).

## Starting the 2-hour class
1. Say **"set up the class"**. It checks Docker and port `8085`, builds/starts `wbl-unix` (`Ubuntu 24.04`), seeds `/workspace/training_lab`, runs `scripts/smoke.sh`, and prints **READY**.
2. Say **"teach class"** (full 2-hour flow) or **"teach module N"** (`1`–`4`).
3. Confirm whether your screen is shared (answers stay hidden until you say `answer`).

## 2-Hour Pacing Budget
| Module | Budget | Focus |
|---|---|---|
| **1** (`0:00–0:25`) | 25 min | Kernel vs Shell, FHS Tree (`/`), `root`, Case Sensitivity, Relative vs Absolute Paths |
| **2** (`0:25–1:00`) | 35 min | Permissions (`rwx`, `644`/`755`, `chmod`), `grep` & Regex, Pipes (`\|`) & Redirection (`>`, `>>`) |
| **3** (`1:00–1:30`) | 30 min | Processes (`ps`, `kill`, `SIGTERM` vs `-9`, `jobs`), Networking (`ip addr`, `ss -tuln`, `ssh`, `rsync`), `apt` & Security |
| **4** (`1:30–2:00`) | 30 min | Bash Scripts (`#!/bin/bash`, `chmod +x`, Variables, `-gt`/`-eq`, `$?`, `&&`/`||`), 2 live `scripts/break.sh` faults |

## During class controls
`next` · `back` · `repeat` · `skip` · `answer` · `more` · `status` (shows elapsed vs 120-min clock) · `take over` · `jump N.M` · `end`

## At the end of class
1. Say `end`. Assign `labs/` + [docs/student-guide.md](docs/student-guide.md) (or `practice-unix`) so candidates review every Beat, practice explaining the **Candidate Takeaways** in their own words, complete the labs + post-class self-study, and send their 8-question quiz **Daily Report**.
2. Run `scripts/fix.sh` (or `scripts/setup.sh --stop`) to clean up.
