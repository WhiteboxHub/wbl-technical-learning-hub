# Module 1 — Unix Architecture, Directory Tree & Paths (25 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **25 minutes** (`0:00–0:25`).
Deck slides: 1–25 (focus on high-impact concepts; skip long Multics trivia).
Story anchor: **The Time-Travelling Workshop (Map & Spoken Orders)** — instead of clicking folders on a desktop, you give precise spoken commands to a workshop where every tool has a name (`ls`, `grep`, `chmod`), every shelf has an exact address (`/` -> `/workspace/training_lab`), and small tools snap together like LEGO blocks.
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Explain Kernel vs Shell, navigate the Unix directory tree using relative and absolute paths, prove filename case-sensitivity, and use core file/directory commands safely.

---

### Beat 1.1 — Why Unix, Kernel vs Shell & Core Philosophy (8 min)
- **Slides:** 2–11
- **Say:**
  - Unix was built at Bell Labs by **Ken Thompson** and rewritten in **C** (1973) by **Dennis Ritchie** so the OS became portable across hardware — not trapped on one machine.
  - **2 layers to picture:**
    - **Kernel** (engine room — note Slide 9 image spells it "Kernal", actual spelling **Kernel**): talks directly to CPU, RAM, disks, and network cards.
    - **Shell** (interpreter — e.g., `bash`): translates your typed commands into kernel actions.
  - **3 Unix superpowers:** multiuser & multitasking, **"almost everything is a file"** (documents, directories, even devices under `/dev` and processes under `/proc`), and **"Tools, not towers"** (small focused tools you combine cleanly).
- **Demo (run: agent):** inspect OS/kernel, current shell, and active workspace inside the container.
  ```bash
  scripts/sh.sh "uname -a && echo \"Shell: \$SHELL\" && whoami && pwd"
  ```
  **Point out:** `Linux` kernel running GNU/Linux tools, active shell `/bin/bash`, working directory `/workspace/training_lab`.
- **Candidate takeaway:** *"The Kernel manages hardware; the Shell translates your commands; Unix treats almost everything as a file and favors small composable tools."*
- **Ask:**
  - Q: In Unix, what is the difference between the Kernel and the Shell? — A: The Kernel manages hardware (CPU, memory, disk, devices), while the Shell is the command interpreter between the user and the kernel.
- **Done when:** candidates can explain Kernel vs Shell and what "Tools, not towers" means.

### Beat 1.2 — Directory Tree, Superuser (`root`) & Case Sensitivity (8 min)
- **Slides:** 12–17
- **Say:**
  - Unix uses a **single inverted tree** starting at `/` (**root** directory — distinct from `/root`, the admin user's home!):
    - `/bin` (essential user commands), `/sbin` (superuser commands), `/etc` (configs like `/etc/passwd`), `/home` (user home dirs like `/home/devuser`), `/var` (logs & changing data like `/var/log`), `/tmp` (temporary files), `/dev` (devices).
  - **`root` (UID 0):** the superuser can bypass file permissions — which is why day-to-day work uses a normal user (`devuser`), not `root`.
  - **Case-sensitive:** `Report.txt`, `report.txt`, and `REPORT.txt` are **three separate files** in Unix!
  - *(Slide typo heads-up: Slide 18 shows `/ls`, `/cd`, `/cp` — in the shell, type commands **without** leading `/`: `ls`, `cd`, `cp`. Slide 19 pairs `"show current position"` with `rm` — **`pwd`** shows current directory, while **`rm`** deletes files! Slide 21 says `df show` — the real command is `df -h`.)*
- **Demo (run: agent):** prove top-level FHS tree and case sensitivity live.
  ```bash
  scripts/sh.sh "ls / && echo '---' && ls -la docs/*eport.txt && head -n 2 docs/Report.txt docs/report.txt"
  ```
  **Point out:** `Report.txt` ("Quarterly Summary") and `report.txt` ("Daily Draft") coexist side by side in the same folder without overwriting each other.
- **Candidate takeaway:** *"Unix starts at `/` (root), stores configs in `/etc` and changing logs in `/var`, and treats uppercase vs lowercase filenames as completely different files."*
- **Ask:**
  - Q: If you see `Report.txt` and `report.txt` in the same folder on Linux, is that a filesystem error? — A: No — Unix filesystems are case-sensitive, so they are two distinct files.
- **Done when:** candidates know key directories (`/`, `/etc`, `/var`, `/home`, `/tmp`, `/bin`) and case sensitivity.

### Beat 1.3 — Relative vs Absolute Paths & Core Commands (9 min)
- **Slides:** 18–25
- **Say:**
  - **Command shape:** `command -options arguments` (spaces separate parts; options start with `-` or `--`). Use `man <cmd>` or `<cmd> --help` anytime!
  - **Absolute Path:** starts with `/` (e.g., `/etc/passwd`, `/workspace/training_lab/docs/readme.txt`). Always points to the exact same file regardless of where you currently stand (`pwd`). Essential for cron jobs, scripts, and `ln -s` symlinks!
  - **Relative Path:** depends on `pwd` using `.` (here) and `..` (parent directory), e.g., `../config/app.conf` or `../../`.
  - **Daily file ops:** `ls -la`, `cd`, `pwd`, `cp`, `mv` (move OR rename), `rm` (permanent — no Recycle Bin!), `mkdir -p`, `rmdir`, `cat` (short files), `less` / `head` / `tail` (long files).
- **Demo (run: agent):** navigate via relative path, read via absolute path, then safely copy/rename/clean up inside `tmp/`.
  ```bash
  scripts/sh.sh "cd /workspace/training_lab/docs && pwd && cat ../config/app.conf && head -n 2 /etc/passwd"
  scripts/sh.sh "mkdir -p tmp/demo && cp docs/readme.txt tmp/demo/ && mv tmp/demo/readme.txt tmp/demo/notes.txt && ls -l tmp/demo && rm -r tmp/demo"
  ```
  **Point out:** `../config/app.conf` only worked because we were in `docs/`, whereas `/etc/passwd` works from anywhere.
- **Candidate takeaway:** *"Absolute paths start with `/` and work from anywhere; relative paths use `.` and `..` from `pwd`; `rm` removes immediately without a trash bin."*
- **Ask:**
  - Q: When writing an automated script or symlink (`ln -s`), should you rely on relative paths or absolute paths? — A: Absolute paths (starting with `/`), because automated scripts may be invoked from any working directory.
- **Done when:** candidates switch between relative and absolute paths without confusion.

---

## Post-Class Practice (Candidates)
Complete [labs/module-01-architecture-paths-nav.sh](../../labs/module-01-architecture-paths-nav.sh) (~15 min after class).
