# Self-Study 2 — `systemd`, Cron, Security Hardening & 2 a.m. Linux Incident Playbook (Levels 4–7)

> **For Candidates & AI Agents:** Study this **after** Self-Study 1. It covers how Linux runs services (`systemd` & `journalctl`), scheduled jobs (`cron`), security/firewall administration (`sudo`, `/etc/shadow`, SSH keys, `ufw`), backups (`tar`), and resource/incident triage.

---

### O1 — Service Management (`systemd` + `journalctl`) & `cron` Scheduling
- **1. Why `systemd` Replaces Background `&` in Production:**
  - Running `python3 app.py &` stops when your SSH shell closes or the server reboots. Real Linux servers manage long-running apps via **systemd unit files** (`/etc/systemd/system/myapp.service`) supervised by **PID 1**.
  - **Essential commands (usually require `sudo` for start/stop/enable):**
    - `systemctl status myapp` — is it `active (running)` or `failed`?
    - `sudo systemctl restart myapp` / `sudo systemctl reload myapp`
    - `sudo systemctl enable myapp` — start automatically after reboot (fixing *"service failed after reboot"*!).
    - `journalctl -u myapp -n 50 --no-pager` / `journalctl -u myapp -f` — inspect service logs + startup errors!
- **2. Scheduled Automation (`cron` — Slide 52):**
  - 5-field `crontab` syntax (`crontab -l`, `crontab -e`): `min hour day month weekday command`
    ```text
    30 2 * * *  /workspace/training_lab/bin/backup.sh >> /workspace/training_lab/tmp/cron.log 2>&1
    ```
  - **3 Classic Cron Failure Traps:** (1) minimal non-interactive `$PATH` (always use **absolute paths** like `/workspace/training_lab/bin/backup.sh`), (2) swallowed errors without `>> logfile 2>&1`, (3) overlapping runs if a job hangs (guard with `flock` or lockfile).
- **Check Q:** Your API works fine when started manually, yet disappears after a server reboot — what `systemctl` command was forgotten? — **A:** `sudo systemctl enable <service>` (so `systemd` starts the unit at boot).

---

### O2 — Secure Access, `/etc/shadow`, `sudo`, SSH Keys, `tar` & Firewalls
- **User & Password Security (root-only files):**
  - `/etc/passwd` (world-readable UID/GID/home/shell list) vs **`/etc/shadow`** (salted password hashes + expiry — readable **only by `root`**!).
  - **`/etc/group`** lists supplementary group memberships (`usermod -aG sudo devuser`).
  - **`sudo`** (configured safely via `sudo visudo` -> `/etc/sudoers`): grants specific least-privilege commands without sharing the `root` password.
- **SSH Key Authentication (Slides 38, 42):**
  - `ssh-keygen -t ed25519` -> copy `~/.ssh/id_ed25519.pub` into server's `~/.ssh/authorized_keys`.
  - Strict permissions required by OpenSSH: `chmod 700 ~/.ssh` and `chmod 600 ~/.ssh/authorized_keys` (plus `PermitRootLogin no` & `PasswordAuthentication no` in `/etc/ssh/sshd_config`).
- **Backups (`tar`) & Delta Sync (`rsync` vs `scp`):**
  - Create archive: `tar -czvf config-backup.tar.gz config/` | Inspect: `tar -tzvf config-backup.tar.gz` | Extract: `tar -xzvf config-backup.tar.gz`.
  - Use `rsync -avz src/ user@host:/dest/` for incremental deployments/backups instead of re-copying unchanged files with `scp`.
- **Firewall Awareness (`ufw` on Ubuntu):** `sudo ufw status`, `sudo ufw allow 22/tcp`, `sudo ufw allow 80,443/tcp` (never open database ports `3306`/`6379` to `0.0.0.0/0`!).
- **Check Q:** Why does OpenSSH ignore `~/.ssh/authorized_keys` if permissions are `666`? — **A:** Loose permissions allow other local users to overwrite keys, so SSH enforces `700` on `~/.ssh` and `600` on key files.

---

### O3 — Storage, Memory, Open File Descriptors & Log Rotation
- **Real-world disk & memory traps:**
  - **RAM (`free -h`):** check the **`available`** column — Linux uses spare RAM for filesystem page cache, so low `"free"` isn't an outage unless `"available"` nears zero and Swap thrashes (`vmstat`/`iostat`).
  - **Load Average (`top` / `uptime`):** 1m / 5m / 15m average runnable+uninterruptible tasks; compare against CPU core count (`nproc`).
  - **Deleted-but-Open Log File:** If you `rm` an active 10 GB log without restarting/reloading the process holding it open, **`df -h` stays at 100%!** Find held deleted files with `sudo lsof +L1`, then gracefully reload the service (`logrotate` handles this with `postrotate` reload/HUP or `copytruncate` automatically).
- **Mounting & `/etc/fstab`:** `lsblk` inspects disks/partitions; `/etc/fstab` defines persistent mounts across reboots (`mount`/`umount` require `sudo`).
- **Check Q:** You deleted a 15 GB log file, yet `df -h` still reports the disk at 100%. Why, and how do you reclaim the space? — **A:** A running process still holds an open file descriptor to that deleted file; find it with `lsof +L1` and restart/reload that process (never crash critical DBs with `kill -9`).

---

### O4 — The 5-Minute 2 a.m. Linux Incident Playbook
Run these 5 checks in order before guessing:
1. **Disk & Inodes:** `df -h && df -i` -> isolate big folders with `du -sh /var/* /workspace/* | sort -h`.
2. **CPU, RAM & Runaway PID:** `free -h && ps aux --sort=-%cpu | head` -> check `R/S/T/Z` state (`top`).
3. **Ports & Bind Address:** `ss -tuln` -> confirm service listens on `0.0.0.0:<port>` (not `127.0.0.1` only!).
4. **Permissions, Ownership & CRLF:** `ls -l <file>` (`+x`? right user?) and check for `\r\n` (`^M`).
5. **Logs & Service Status:** `systemctl status <svc>` / `journalctl -u <svc> -n 50` / `grep -cE "ERROR|FATAL" logs/app.log`.

---

## Self-Study Quiz Bank (For AI Quiz Mode)
1. Compare `systemctl restart` vs `systemctl enable` — what problem happens on reboot if you skip `enable`?
2. Write a `crontab` entry running `/workspace/training_lab/bin/backup.sh` every weekday at `02:30` and logging stdout+stderr.
3. Why is `/etc/passwd` readable by all users while `/etc/shadow` is `root`-only?
4. When `df -h` stays at `100%` after deleting a huge log file, how do you diagnose and safely reclaim the space?
5. In `free -h`, why is `"available"` a better measure of memory headroom than `"free"`?
6. How do you list contents of a `.tar.gz` archive without extracting it?
7. What two settings in `/etc/ssh/sshd_config` paired with `chmod 600 ~/.ssh/authorized_keys` block password brute-force attacks?
8. An app is listening on `127.0.0.1:8080` in `ss -tuln` — why do requests from another server or container fail?
