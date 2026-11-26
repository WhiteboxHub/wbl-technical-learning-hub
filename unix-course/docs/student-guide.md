# Student Guide — Unix & Shell Scripting (2-Hour Class + AI Self-Study)

Master the high-impact Unix & Linux CLI skills taught in your 2-hour class — and use **ChatGPT, Claude, Antigravity, or any AI coding agent** afterward to practice explaining every concept clearly, run real commands inside an Ubuntu 24.04 container (`/workspace/training_lab`), and test yourself with quizzes.

---

## 1. Curriculum Roadmap (What You Will Explain & Build)
| # | Module | You will be able to… |
|---|---|---|
| **1** | Architecture, Directory Tree & Paths | Explain Kernel vs Shell, map `/etc`, `/var`, `/home`, `/tmp`, `/bin`, prove case sensitivity, and switch cleanly between relative (`.`, `..`) and absolute (`/`) paths |
| **2** | Permissions, `grep` & Unix Pipes | Decode `-rw-r--r--` / `755` / `644`, fix `Permission denied` with `chmod`/`chown`, query logs with `grep -i/-v/-n/-c/-r/-E/-F`, and chain `grep \| awk \| sort \| uniq -c` |
| **3** | Processes, Networking, Packages & Security | Read `ps aux` (`R/S/T/Z`), kill cleanly (`SIGTERM` vs `-9`), inspect ports (`ss -tuln` / `ip addr`), pick `rsync` vs `scp`, and enforce Least Privilege (`sudo`, `/etc/shadow`, SSH keys) |
| **4** | Bash Scripting, Exit Codes & Live Faults | Write executable Bash scripts (`#!/bin/bash`, variables, `$(( ))`, `-eq/-gt`, `if/else/fi`), inspect `$?`, handle errors (`&&`/`\|\|`), and diagnose `scripts/break.sh` faults |
| **Self-Study** | [Toolkit](../course/self-study/01-unix-daily-engineering-toolkit.md), [Ops & Cron](../course/self-study/02-unix-ops-cron-troubleshooting.md) & [Backend/Scenarios](../course/self-study/03-backend-devops-production-labs.md) | Master `find`, `df -i` inodes, `free -h`, `awk`/`sed`/`cut`/`tee`, Hard vs Soft links, `umask`/SUID/Sticky bit, `systemctl`/`journalctl`, `cron`, Nginx proxy, Docker internals, 12 production scenarios & Interview Bank |

---

## 2. Get Your Laptop Ready (Optional Ubuntu Docker Sandbox)
Works identically on Windows (Git Bash / WSL2), macOS, and Linux!
1. Start **Docker Desktop**, then inside `unix-course/` run:
   ```bash
   scripts/setup.sh
   ```
   (Or in Claude Code / Antigravity, say **"set up my environment"**.)
2. Run your first command inside `/workspace/training_lab`:
   ```bash
   scripts/sh.sh "pwd && ls -la docs/ && grep -c 'ERROR' logs/app.log"
   ```
3. Open an interactive Linux terminal anytime: `scripts/sh.sh`
   Reset workspace: `scripts/setup.sh --reset` | Stop: `scripts/setup.sh --stop`.

---

## 3. Study With ChatGPT or Any AI Coding Agent (Even Without Docker)
- **In Claude Code / Antigravity / Cursor:** say **"start learning"**, **"explain module 1"**, **"help with the exercise"**, or **"quiz me"** (`practice-unix` loads automatically).
- **In ChatGPT / Gemini Web:** paste the GitHub link to `wbl-technical-learning-hub/unix-course` (or upload the folder) with this copy-paste prompt:
  ```text
  Read AGENTS.md, docs/learning-plan.md, docs/lab-reference.md, course/modules/, and course/self-study/.
  Guide me through Module [1 / 2 / 3 / 4] (and course/self-study/ afterward) using the 4-stage loop:
  1. Teach ONE Beat at a time (Why & Story Anchor -> Rule, Internals & output -> Recap & Takeaway) and ask 1 check question — WAIT for my reply before advancing.
  2. Walk through labs/ one task at a time (make me predict counts/outputs first; 4-Rung Hint Ladder, never give finished solutions).
  3. Run an 8-question quiz one question at a time (no answers until the end), then output my score, weak areas, and DAILY REPORT.
  ```

The AI agent follows the **4-Stage Loop**:
1. **Tutor:** Explains 1 Beat with its Story Anchor -> gives the **Candidate Takeaway** -> asks you to explain it back or answer 1 check question.
2. **Practice:** Walks you through `labs/module-01-*.sh` … `04-*.sh` one task at a time (predict counts/outputs first!).
3. **Coding Coach:** Reviews your commands & Bash scripts using the **4-Rung Hint Ladder** (hints before solutions).
4. **Quiz & Evaluate:** Asks 8 questions one at a time (no early answers), scores you, lists weak areas, and outputs your **`DAILY REPORT`**:
   `DAILY REPORT - [Name] - [Date] | Module: __ | Labs: [Done/Partial] | Score: __/8 | Weak areas: [...] | Open Qs: [...]`

---

## 4. High-Impact Unix & Bash Cheat Sheet
```bash
# Relative vs Absolute paths & safe file inspection
pwd && ls -la && head -n 5 /etc/passwd

# Fix permissions cleanly (never blindly 777)
chmod 755 bin/onboarding_helper.sh

# Fast log triage & top failing SSH IPs
grep -cE 'ERROR|FATAL' logs/app.log
grep 'Failed password' logs/auth.log | awk '{print $(NF-3)}' | sort | uniq -c | sort -nr

# Processes & listening ports
ps aux | grep http.server
ss -tuln || netstat -tuln

# Clean Bash guardrails
#!/usr/bin/env bash
set -euo pipefail
errs=$(grep -c 'ERROR' /workspace/training_lab/logs/app.log)
[ "$errs" -gt 10 ] && echo "ALERT: $errs" || echo "OK"
```
