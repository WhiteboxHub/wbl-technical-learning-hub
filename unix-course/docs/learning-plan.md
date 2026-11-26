# Structured Step-by-Step Learning Plan (For Candidates & AI Agents)

> **To any AI Agent (ChatGPT, Claude, Antigravity, Codex, Cursor, Gemini) reading this repo:**
> When a candidate shares this repository and asks to learn Unix & Shell Scripting step by step, **follow this exact 4-Module curriculum (+ Post-Class Self-Study 1–2), teaching protocol, and evaluation flow**. Teach one Beat at a time, ask them to explain concepts back in their own words, and never solve lab exercises or scripts for them.

---

## How the 4-Phase AI Study Loop Works (Per Module)

### Phase 1 — Structured Topic Explanation (Tutor Mode)
1. Check `candidate-state.md` (if absent, start at Module 1 or ask which module their instructor covered).
2. Read `course/modules/01-*.md` through `04-*.md` first (then `course/self-study/01-*.md` through `03-*.md` afterward).
3. Teach **one Beat/section at a time** in this structured coaching sequence:
   - **Definition & Why It Exists:** simple explanation + problem it solves + the module's **Story Anchor**.
   - **Internals, Rule & Output:** exact Linux/Bash mechanism (noting `sudo`/root needs & slide clarifications) + concrete `/workspace/training_lab` command and expected output + 1 common mistake/security trap.
   - **Recap & Takeaway:** 3 short bullets + the Beat's **Candidate Takeaway**.
4. **Check Understanding (Pause Required):** Ask **1 Check Question** (or ask the candidate to explain the takeaway in their own words) and **wait for their reply before moving on**.

### Phase 2 — Hands-On Shell & Bash Practice (Practice Mode)
1. Use `labs/module-01-*.sh` … `04-*.sh`, one task at a time.
2. **Prediction Rule:** Before running/checking any `wc -l`, `grep -c`, pipe, `chmod`, or Bash conditional command, make the candidate predict the expected count or output using [docs/lab-reference.md](lab-reference.md).
3. Ask 1 follow-up "why" question before marking the task Completed.

### Phase 3 — Shell Review & Hint-First Debugging (Coding Coach Mode)
1. Compare candidate commands/scripts privately against `solutions/module-01-*.sh` … `04-*.sh`.
2. Review in order: syntax/shebang -> quoting (`"$var"`), permissions (`chmod 755` vs `777`), `sort | uniq -c`, `[ "$x" -gt 10 ]` vs `>`, `$?` handling -> readability -> 1–2 improvements.
3. Use the **4-Rung Hint Ladder** (expected vs actual -> conceptual cause -> partial command/script skeleton -> fix + follow-up task).

### Phase 4 — Evaluation, Weak-Area Diagnosis & State Update (Quiz Mode)
1. Ask **8 questions ONE at a time** mixing conceptual, "explain in your own words", 2 a.m. incident scenario, and predict-count / exit-code questions.
2. **NEVER reveal answers or hints while the quiz is running.**
3. **After question 8 only:** output `QUIZ RESULT` (score, per-topic breakdown, missed explanations, priority weak areas), `UPDATED CANDIDATE STATE`, and `DAILY REPORT` ([docs/student-guide.md](student-guide.md)).

---

## Roadmap & Exit Gates

| Stage | File | Topics Covered | Exit Gate (What Candidate Can Explain & Demonstrate) |
|---|---|---|---|
| **1** | `01-architecture-paths-navigation.md` | Kernel vs Shell, FHS Tree (`/`), `root`, Case Sensitivity, Relative (`.`, `..`) vs Absolute paths | Prove `Report.txt != report.txt`, switch relative/absolute paths cleanly, manipulate temp files safely |
| **2** | `02-permissions-grep-pipes.md` | `u/g/o`, `rwx` (`4/2/1`), `chmod 755`/`644`, `chown`/`chgrp`, `grep -i/-v/-n/-r/-c/-E/-F`, Regex (`^`, `$`, `[0-9]`), Pipes (`\|`), `sort \| uniq -c`, Redirection (`>`, `>>`, `tee`) | Fix `Permission denied` without `777`, query `logs/app.log` & `auth.log`, chain 3+ pipe stages |
| **3** | `03-processes-networking-security.md` | Process states (`R/S/T/Z`), `ps aux`, `kill` (`SIGTERM`) vs `kill -9`, `jobs`/`fg`/`nice`, `ip addr`, `ss`/`netstat -tuln`, `ssh`/`scp`/`rsync`, `apt`, `sudo` & `/etc/shadow` | Inspect/terminate background worker cleanly, verify port `8080` listening, read `sshd_config.sample` |
| **4** | `04-bash-scripting-fault-labs.md` | `.bashrc`, `#!/bin/bash`, `chmod +x`, Variables/`read -p`, `$(( ))`, `-eq/-ne/-gt/-lt`, `if/elif/else`, `$?`, `&&`/`\|\|`, Live `scripts/break.sh` faults + Capstone | Write threshold & `servers.csv` audit scripts with exit codes, diagnose `bad-perms` & `runaway-proc` |
| **Self-Study 1** | [01-unix-daily-engineering-toolkit.md](../course/self-study/01-unix-daily-engineering-toolkit.md) | `find`, `type`/`which`, `df -i` inodes, `free -h`, `awk`/`sed`/`cut`/`tr`/`tee`, Hard vs Soft Links, `umask`/SUID/Sticky Bit, `$PATH`, Bash args/functions/`trap`/`set -euo pipefail` | Filter `servers.csv` with `awk`, debug `df -i`/CRLF/links, write `trap`-safe Bash |
| **Self-Study 2** | [02-unix-ops-cron-troubleshooting.md](../course/self-study/02-unix-ops-cron-troubleshooting.md) | `systemctl` & `journalctl`, 5-field `cron`, SSH keys (`chmod 600`), `/etc/shadow`/`sudo`/`ufw`, `rsync -avz` vs `scp`, `tar -czvf`, deleted-open-FD recovery (`lsof`), Incident Playbook | Enable reboot-safe service, write safe `crontab` line, debug deleted open logs & ports |
| **Self-Study 3** | [03-backend-devops-production-labs.md](../course/self-study/03-backend-devops-production-labs.md) | Backend service ownership, `.env` secrets, Nginx reverse proxy (`127.0.0.1` vs `0.0.0.0`), Docker namespaces/cgroups, 12 production triage scenarios & Tiered Interview Bank | Diagnose all 12 production incident cases and pass Beginner/Intermediate/Senior checks |
