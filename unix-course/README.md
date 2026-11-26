# Unix & Shell Scripting Essentials — 2-Hour Class + AI Self-Study Repo

Running example: **Ubuntu 24.04 Unix Training Lab** (`/workspace/training_lab` with `docs/`, `logs/app.log` 120 lines, `logs/auth.log` 30 lines, `bin/`, `config/`, `archive/`, `tmp/`, plus `devuser`) — optimized for **Instructors** (a tight **2-hour live class** with zero filler) and **Candidates** (step-by-step study, concept explanation practice, Bash/command coaching, and quizzes in **ChatGPT, Claude, Antigravity, Codex, Cursor, or any AI agent**).

---

## Guides & Learning Roadmap
- **[Structured Learning Plan](docs/learning-plan.md)** — 4-stage AI study loop, prediction rules, evaluation, and exit gates
- **[Student Guide](docs/student-guide.md)** — laptop setup, Unix/Bash cheat sheet, and AI self-study flow
- **[Lab Reference](docs/lab-reference.md)** — directory tree map and exact seeded line/file counts
- **[Course Table of Contents](docs/course-toc.md)** — 2-hour module budget + post-class self-study packs
- **[Instructor Guide](docs/instructor-guide.md)** & **[Class-Day Quick Start](docs/class-day-quickstart.md)** — setup and 120-minute live pacing controls

---

## Paste Into ChatGPT or Any AI Coding Agent (Candidates)
1. Open in **Claude Code / Antigravity / Cursor** (loads `.claude/skills/practice-unix/SKILL.md` automatically) OR paste the GitHub link / folder into **ChatGPT / Claude Web / Gemini** with the starter prompt in **[docs/student-guide.md](docs/student-guide.md)**.
3. The AI agent will:
   - Explain each Beat clearly using its **Story Anchor**, `/workspace/training_lab` example, and plain-English **Candidate Takeaway**
   - Ask you to explain concepts back in your own words before moving on
   - Coach your commands and Bash scripts in `labs/` using the **4-Rung Hint Ladder** (hints before solutions)
   - Quiz you one question at a time, diagnose weak areas, and output your **`CANDIDATE STATE`** + **`DAILY REPORT`**

---

## Start the Local Ubuntu Unix Lab Container (Optional / Recommended for Hands-On CLI)
Requires **Docker Desktop** running. Give Windows, Mac, and Linux users the **identical Ubuntu 24.04 environment**.

```bash
scripts/setup.sh
```

- **Interactive Linux Shell:** `scripts/sh.sh` (drops straight into `/workspace/training_lab`)
- **Run One Command:** `scripts/sh.sh "grep -c 'ERROR' logs/app.log"`
- **Lab HTTP Listener (for `ss`/`netstat`/`curl` demos):** http://localhost:8085/readme.txt (container port `:8080`)
- **Reset to clean seed:** `scripts/setup.sh --reset` | **Stop:** `scripts/setup.sh --stop`

---

## 2-Hour Course Modules (4 Focused Modules = 120 Minutes)
| # | Module | 2-Hr Budget | Key High-Impact Topics |
|---|---|---|---|
| 1 | [Unix Architecture, Directory Tree & Paths](course/modules/01-architecture-paths-navigation.md) | 25 min | Kernel vs Shell, FHS (`/`, `/bin`, `/etc`, `/home`, `/var`, `/tmp`, `/dev`), `root` vs user, Case Sensitivity, Relative (`.`, `..`) vs Absolute paths |
| 2 | [Permissions, `grep` & Unix Pipes](course/modules/02-permissions-grep-pipes.md) | 35 min | `u/g/o`, `rwx` (`4/2/1`), `chmod 755`/`644`, `grep -i/-v/-n/-r/-c/-E/-F`, Regex (`^`, `$`, `[0-9]`, `.*`), Pipes (`\|`), `sort \| uniq -c`, Redirection (`>`, `>>`, `2>`) |
| 3 | [Processes, Networking, Packages & Security](course/modules/03-processes-networking-security.md) | 30 min | PID/States (`R/S/T/Z`), `ps aux`, `kill` (`SIGTERM`) vs `kill -9`, `jobs`/`fg`/`bg`/`nice`, `ip addr`, `ss`/`netstat -tuln`, `ssh`, `scp`/`rsync`, `apt`, Least Privilege |
| 4 | [Bash Scripting, Exit Codes & Live Fault Triage](course/modules/04-bash-scripting-fault-labs.md) | 30 min | `.bashrc`, `#!/bin/bash`, `chmod +x`, Variables/`read -p`, `$(( ))`, `-eq/-ne/-gt/-lt`, `if/elif/else`, `$?`, `&&`/`||`, Live `scripts/break.sh` faults |

### Post-Class Candidate Self-Study (Outside the 2-Hour Live Clock)
- **[Self-Study 1: Daily Engineering Toolkit](course/self-study/01-unix-daily-engineering-toolkit.md)** — `find`, `type`/`which`, `df -i` inodes, `free -h`, practical `awk`/`sed`/`cut`/`tr`/`tee`, Hard vs Soft Links, `umask`/SUID/Sticky Bit, `$PATH`, Bash args/functions/`trap`/`set -euo pipefail`.
- **[Self-Study 2: `systemd`, Cron & Incident Playbook](course/self-study/02-unix-ops-cron-troubleshooting.md)** — `systemctl` & `journalctl`, 5-field `cron` scheduling, `/etc/shadow`/`sudo`/SSH keys/`ufw`, `rsync -avz`, `tar`, deleted-open-FD recovery (`lsof`), and the 5-step incident playbook.
- **[Self-Study 3: Backend/DevOps, 12 Scenarios & Interview Bank](course/self-study/03-backend-devops-production-labs.md)** — app user isolation, `.env` secrets, Nginx reverse proxy (`127.0.0.1` vs `0.0.0.0` in Docker), Linux namespaces/cgroups, 12 production troubleshooting scenarios, and Beginner/Intermediate/Senior interview Q&As.

---

## Layout
```text
unix-course/
├── AGENTS.md                  # Universal AI instructions (ChatGPT, Codex, Antigravity, Cursor, Claude)
├── CLAUDE.md                  # Claude Code entrypoint
├── instructor-steps.md        # 2-hour instructor runbook & pacing controls
├── docker-compose.yml         # Ubuntu 24.04 Unix Lab (:8085 -> :8080)
├── docker/                    # Dockerfile + deterministic workspace seeder (init-lab.sh)
├── .claude/skills/            # setup-unix-class, teach-unix-class (2-hr timer), setup-candidate, practice-unix
├── course/
│   ├── modules/               # 4 tight 2-hour modules (Story Anchors, Candidate Takeaways, Demos, Q&As)
│   └── self-study/            # High-ROI post-class Unix & Linux Ops self-study packs
├── labs/                      # 4 post-class hands-on shell & Bash lab starters (+ Capstone)
├── solutions/                 # 4 separated reference solutions (never shown before attempt)
├── scripts/                   # setup.sh, smoke.sh, sh.sh, break.sh, fix.sh
└── docs/                      # learning-plan, lab-reference, course-toc, instructor & student guides
```
