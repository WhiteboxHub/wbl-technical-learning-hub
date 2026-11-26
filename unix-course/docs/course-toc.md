# Unix & Shell Scripting Essentials — 2-Hour Class Table of Contents

Designed for a **2-hour (120-minute) live instructor session** + **structured AI-guided candidate self-study** (`/workspace/training_lab` in Ubuntu 24.04 Docker container).
Low-ROI trivia (extended Multics/PDP-7 history, `mount`/`umount` hardware formatting drills, writing complex `awk` parsers or PAM modules live) is intentionally trimmed or moved to post-class self-study so every live minute covers high-signal daily Linux engineering skills.

| # | Module | 2-Hr Budget | Topics Covered (High-Impact Only) | Lab File |
|---|---|---|---|---|
| **1** | Unix Architecture, Directory Tree & Paths | **25 min** (`0:00–0:25`) | Kernel vs Shell, Unix philosophy, FHS Tree (`/`, `/bin`, `/etc`, `/home`, `/var`, `/tmp`, `/dev`, `/sbin`), `root` vs `devuser`, Case Sensitivity, Relative (`.`, `..`) vs Absolute paths | [01-architecture-paths-navigation.md](../course/modules/01-architecture-paths-navigation.md) |
| **2** | Permissions, `grep` & Unix Pipes | **35 min** (`0:25–1:00`) | `u/g/o`, `rwx` (`4/2/1`), `chmod 755`/`644`, `chown`/`chgrp`, `grep` (`-i/-v/-n/-r/-c/-E/-F`), Regex (`^`, `$`, `[0-9]`, `.*`), Pipes (`\|`), `sort \| uniq -c`, Redirection (`>`, `>>`, `2>`, `tee`) | [02-permissions-grep-pipes.md](../course/modules/02-permissions-grep-pipes.md) |
| **3** | Processes, Networking, Packages & Security | **30 min** (`1:00–1:30`) | PID/PPID/States (`R/S/T/Z`), `ps aux`, `kill` (`SIGTERM`) vs `kill -9`, `pkill`, `&`/`jobs`/`fg`/`nice`, `ip addr`, `ss`/`netstat -tuln`, `ssh`/`scp`/`rsync`, `apt`, `sudo` & `/etc/shadow` | [03-processes-networking-security.md](../course/modules/03-processes-networking-security.md) |
| **4** | Bash Scripting, Exit Codes & Live Fault Triage | **30 min** (`1:30–2:00`) | `.bashrc`, `#!/bin/bash`, `chmod +x`, Variables/`read -p`, `$(( ))`, `-eq/-ne/-gt/-lt`, `if/elif/else`, `$?`, `&&`/`\|\|`, 2 live `scripts/break.sh` faults | [04-bash-scripting-fault-labs.md](../course/modules/04-bash-scripting-fault-labs.md) |

## Post-Class Candidate Self-Study (Outside the 2-Hour Clock)
| # | Pack | Target Timing | High-ROI Topics Covered | File |
|---|---|---|---|---|
| **U1** | Daily Engineering Toolkit | After Modules 1–4 | `find`, `type`/`which`, `df -i` inodes, `free -h`, practical `awk`/`sed`/`cut`/`tr`/`tee`, Hard vs Soft Links, `umask`/SUID/Sticky Bit, `$PATH`, Bash args/functions/`trap`/`set -euo pipefail` | [01-unix-daily-engineering-toolkit.md](../course/self-study/01-unix-daily-engineering-toolkit.md) |
| **U2** | `systemd`, Cron & Incident Playbook | After Module 4 | `systemctl` & `journalctl`, 5-field `cron` syntax & traps, SSH keys (`chmod 600`), `/etc/shadow`/`sudo`/`ufw`, `rsync -avz`, `tar -czvf`, `lsof +L1`, 5-step Incident Playbook | [02-unix-ops-cron-troubleshooting.md](../course/self-study/02-unix-ops-cron-troubleshooting.md) |
| **U3** | Backend/DevOps, 12 Scenarios & Interview Bank | Production & Prep | Service user ownership, `.env` secrets, Nginx reverse proxy (`127.0.0.1` vs `0.0.0.0`), Docker namespaces/cgroups, 12 production scenarios, Tiered Interview Q&As | [03-backend-devops-production-labs.md](../course/self-study/03-backend-devops-production-labs.md) |

## Slide Clarifications (Embedded in Beats)
- **Slide 9 diagram:** Reads "Kernal" -> standard spelling is **Kernel**.
- **Slide 18 (`/ls`, `/cd`, `/cp`):** Commands are run **without** leading slashes (`ls`, `cd`, `cp`).
- **Slide 19 (`show current position -> rm`):** **`pwd`** shows current position; **`rm`** removes files!
- **Slide 21 (`df show`):** Real Linux command is **`df -h`** (or `df`).
- **Slide 33 (`fg <joab_number>`):** Real syntax is **`fg %<job_number>`**.
- **Slide 34 (`Process Priority and C++`):** Means CPU priority (**`nice` / `renice`**), not C++.
- **Slide 48 (`egrep` / `fgrep`):** Deprecated on modern Linux; prefer **`grep -E`** / **`grep -F`**.
- **Slide 58 Arithmetic:** Inside `$(( ... ))`, `*` is multiplication and `**` is exponentiation.
