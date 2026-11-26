# Module 3 — Processes, Networking, Packages & Security (30 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **30 minutes** (`1:00–1:30`).
Deck slides: 31–42 (high-ROI commands cleanly modernized where slides mention legacy/typo syntax).
Story anchor: **The Running Assembly Line & The Network Gates** — files sit on shelves, while **processes** are workers currently executing on CPU with unique IDs (`PID`). Networking tools inspect how workers talk across ports (`TCP/IP`), and security locks keep doors scoped to least privilege.
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Inspect and manage Unix processes (`ps`, `kill`, `SIGTERM` vs `SIGKILL`, `jobs`/`bg`/`fg`/`nice`), run essential network checks (`ip addr`, `ss`/`netstat`, `ping`, `ssh`, `scp`/`rsync`), and apply package/security basics (`apt`, least privilege, SSH key auth).

---

### Beat 3.1 — Processes, States, Signals & Job Control (11 min)
- **Slides:** 31–34
- **Say:**
  - Every running program gets a unique **PID** and a **Parent PID (`PPID`)**, rooted at **PID 1** (`init`/`systemd`).
  - **4 Process States (`ps aux` `STAT` column):**
    - **R (Running):** actively on CPU or runnable.
    - **S (Sleeping):** waiting for I/O or timer (normal for servers!).
    - **T (Stopped):** paused (`Ctrl+Z`).
    - **Z (Zombie):** finished running, waiting for its parent to read its exit code (reaped only by fixing/restarting the parent — **`kill -9` cannot kill an already-dead Zombie!**).
  - **Signals (`kill` vs `kill -9`):** `kill <PID>` sends **`SIGTERM (15)`** (asks nicely so the app flushes buffers/closes DB connections); **`kill -9 <PID>` (`SIGKILL`)** terminates immediately at the kernel level — last resort only! `pkill <name>` targets by process name.
  - **Background/Priority:** `&` starts in background; `jobs`, `bg`, `fg %<job_number>` *(note Slide 33 typo `fg <joab_number>`)*; `nice -n 10 cmd` / `renice -n 5 <PID>` adjust CPU priority *(note Slide 34 header says `"C++"` by mistake — it is CPU scheduling niceness!)*.
- **Demo (run: agent):** inspect `ps aux`, launch a background worker, check `jobs`, and terminate cleanly with `kill`.
  ```bash
  scripts/sh.sh "ps aux | head -n 10"
  scripts/sh.sh "sleep 60 & jobs -l && PID=\$! && ps -p \$PID -o pid,ppid,stat,cmd && kill \$PID && wait \$PID 2>/dev/null || true"
  ```
  **Point out:** PID `1` owns the container startup chain, and `kill $PID` sends graceful `SIGTERM` (`15`), not brutal `-9`.
- **Candidate takeaway:** *"Always try graceful `kill <PID>` (`SIGTERM`) before `kill -9` (`SIGKILL`); Zombie processes are already dead and waiting on their parent."*
- **Ask:**
  - Q: Why try `kill <PID>` before `kill -9 <PID>` on a stuck application server? — A: `kill` sends `SIGTERM`, letting the process close files, flush logs, and drop DB connections cleanly; `kill -9` kills instantly with zero cleanup.
- **Done when:** candidates distinguish `SIGTERM` vs `SIGKILL` and explain the 4 process states.

### Beat 3.2 — Networking Inspection, Listening Ports & Transfers (11 min)
- **Slides:** 35–38
- **Say:**
  - When a service won't connect in Docker or EC2, isolate the layer in order:
    1. **Local interface/IP:** `ip addr` (replaces older `ifconfig`).
    2. **Reachability & route:** `ping <host>` (ICMP reachability), `traceroute <host>` (hop-by-hop path), `nslookup` / `dig` (DNS).
    3. **Is my server actually listening?** **`ss -tuln`** (or **`netstat -tuln`** — `-t` TCP, `-u` UDP, `-l` listening, `-n` numeric ports). Shows `0.0.0.0:8080` vs `127.0.0.1:8080` (**localhost-only traps external Docker traffic!**).
    4. **Remote access & copy:** `ssh user@host`, `tcpdump -i eth0` (packet capture), **`scp`** (simple one-shot SSH file copy) vs **`rsync -avz`** (delta transfer — only sends changed chunks/files, resumable!).
- **Demo (run: agent):** inspect container IP, listening sockets (`8080`), and probe the local docs server cleanly.
  ```bash
  scripts/sh.sh "ip -br addr && echo '---' && (ss -tuln || netstat -tuln) && echo '---' && curl -sI http://localhost:8080/readme.txt | head -n 4"
  ```
  **Point out:** `:8080` is listening (`LISTEN` state) inside the container and mapped to host `:8085` by `docker-compose.yml`.
- **Candidate takeaway:** *"Check `ss -tuln` (or `netstat -tuln`) first to prove what port is listening and on which address (`0.0.0.0` vs `127.0.0.1`); use `rsync -avz` over `scp` for large/repeated syncs."*
- **Ask:**
  - Q: What does every letter in `netstat -tuln` (or `ss -tuln`) ask for? — A: TCP (`-t`), UDP (`-u`), Listening sockets only (`-l`), and numeric IPs/ports without slow DNS lookups (`-n`).
- **Done when:** candidates diagnose port-binding and choose `rsync` vs `scp`.

### Beat 3.3 — Package Management (`apt`) & Unix Security Basics (8 min)
- **Slides:** 39–42
- **Say:**
  - **Packages on Ubuntu/Debian (`apt`):** always refresh index first: `sudo apt update` then `sudo apt install <pkg>` (or `sudo apt upgrade`). Inside containers, clean cache afterward (`rm -rf /var/lib/apt/lists/*`) to keep Docker images small.
  - **Security Core (Least Privilege):**
    - Give each service/human their own **UID/GID** (`adduser`/`useradd`, `passwd`), never run apps as `root`; use **`sudo`** only for specific admin tasks.
    - `/etc/passwd` stores public account info (readable by all), while **`/etc/shadow`** stores password hashes (readable only by `root`!).
    - **SSH (`/etc/ssh/sshd_config`) + PAM (`/etc/pam.d/common-password`):** disable `PermitRootLogin`, enforce **SSH keys** (`PasswordAuthentication no`), and monitor `/var/log/auth.log` for brute-force alerts.
- **Demo (run: agent):** compare `root` vs `devuser` identities and inspect the hardened SSH config sample.
  ```bash
  scripts/sh.sh "id && id devuser && grep '^devuser' /etc/passwd && echo '---' && cat config/sshd_config.sample"
  ```
  **Point out:** Every user in `/etc/passwd` has a numeric UID, primary GID, home directory, and login shell (`/bin/bash`); `sshd_config.sample` blocks root & password brute-forcing in two lines.
- **Candidate takeaway:** *"Run `sudo apt update` before installing packages, enforce Least Privilege (`devuser` instead of `root`), and prefer SSH keys (`PasswordAuthentication no`) over passwords."*
- **Ask:**
  - Q: In `/etc/ssh/sshd_config`, which two settings stop root logins and password brute-force attacks? — A: `PermitRootLogin no` and `PasswordAuthentication no` (paired with `PubkeyAuthentication yes`).
- **Done when:** candidates inspect `/etc/passwd` cleanly and explain Least Privilege.

---

## Post-Class Practice (Candidates)
Complete [labs/module-03-processes-networking-security.sh](../../labs/module-03-processes-networking-security.sh) (~15 min after class).
