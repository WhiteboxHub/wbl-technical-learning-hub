# Self-Study 1 — High-ROI Unix Daily Engineering Toolkit (Levels 1–3 & 8)

> **For Candidates & AI Agents:** Study this **after** completing Modules 1–4. It adds the high-value Linux filesystem, text-processing, permission, monitoring, and Bash scripting mechanics that did not fit into the 2-hour live class. Low-value trivia is intentionally excluded.

---

### U1.1 — File Searching, Command Resolution & Resource Checks (`find`, `type`, `df -i`, `free -h`)
- **Why it matters:** `grep` searches *inside* files; **`find`** locates files by name/size/mtime/permissions. On production servers you also check *which binary* runs (`type`/`which`) and verify **RAM, Disk, and Inodes** before blaming application code.
- **High-ROI commands:**
  - `find /workspace/training_lab -name "*.log"` / `find . -type f -perm 0644`
  - `type cd` vs `which grep` — `type` reveals whether a command is a shell **builtin** (`cd`), **alias**, or external binary (`grep`)!
  - `file <path>` & `stat <path>` — real file type (not just extension!) and exact permissions, UID/GID, inode, timestamps.
  - **`df -h`** (free disk blocks), **`df -i`** (**inodes** — millions of tiny session/cache files can exhaust 100% inodes even when `df -h` shows free GBs!), **`du -sh *`** (folder sizes), **`free -h`** (RAM + buffer/cache available vs Swap), **`lsblk`** (block disks/partitions).
  - `tail -n 20 logs/app.log` / `tail -f logs/app.log` — stream live logs as requests arrive.
- **Try it:**
  ```bash
  scripts/sh.sh "find /workspace/training_lab -name '*.sh' -exec ls -l {} + && type cd grep"
  scripts/sh.sh "df -h /workspace && df -i /workspace && free -h"
  ```
- **Check Q:** A server throws `"No space left on device"` even though `df -h` shows 40% free space — what do you run next? — **A:** `df -i` to check **inode exhaustion** (too many tiny files used up every filesystem inode).

---

### U1.2 — Practical Text Processing (`awk`, `sed`, `cut`, `tr`, `tee`)
- **Why it matters:** Columns, CSVs, streaming transforms, and saving logs while still watching terminal output are daily backend/DevOps work.
- **Key patterns on `/workspace/training_lab`:**
  - **`awk` (structured columns):** `awk -F',' 'NR>1 && $4 >= 75 {print $1, $4"%", $5}' docs/servers.csv`
  - **`sed` (stream edits & Windows CRLF fix):** `sed -i 's/\r$//' script.sh` strips `\r` (`^M`) that breaks scripts with `/bin/bash^M: bad interpreter`.
  - **`cut` & `tr`:** `cut -d',' -f1,5 docs/servers.csv` extracts fixed delimiter columns; `tr '[:lower:]' '[:upper:]'` translates/deletes characters.
  - **`tee`:** writes stdout to a file **and** prints it to the terminal (`grep ERROR logs/app.log | tee tmp/errors.log`). Use `tee -a` to append.
- **Try it:**
  ```bash
  scripts/sh.sh "awk -F',' 'NR > 1 && \$4 >= 75 { print \$1, \$4 \"%\", \$5 }' /workspace/training_lab/docs/servers.csv"
  scripts/sh.sh "cut -d',' -f1,5 /workspace/training_lab/docs/servers.csv | head -n 5"
  ```
- **Check Q:** A shell script edited on Windows fails on Ubuntu with `/bin/bash^M: bad interpreter`. What fixes it cleanly? — **A:** `sed -i 's/\r$//' script.sh` (or `dos2unix script.sh`).

---

### U1.3 — Hard vs Soft Links, Special Permissions (`SUID`/`SGID`/Sticky), `umask` & `$PATH`
- **Why it matters:** These 4 topics are classic mid-to-senior Linux interview questions because they reveal whether you actually understand how the Linux filesystem works under the hood.
- **1. Hard Links (`ln`) vs Symbolic/Soft Links (`ln -s`):**
  - Every file's metadata & disk pointers live in an **inode**; filenames are directory labels pointing to an inode.
  - **Hard link (`ln target link`):** second directory entry pointing directly to the **same inode**. Deleting `target` keeps `link` readable! Cannot cross filesystems or link directories.
  - **Symbolic / Soft link (`ln -s /abs/target link`):** shortcut pointing to a **path string**. Works across disks and for directories — but deleting the target leaves a **dangling/broken symlink**.
- **2. Directory `x` Bit & `umask`:**
  - On a **directory**, `r` lists filenames, `w` creates/deletes entries, **`x` lets you `cd` / access paths through it**.
  - **`umask`** (typically `022`) masks default creation bits: new files default to `666 - 022 = 644`, new directories to `777 - 022 = 755`.
- **3. Special Permission Bits:**
  - **SUID (`4xxx`, `rws` on user):** runs as the file owner (e.g., `/usr/bin/passwd` runs as `root` so normal users can update `/etc/shadow`).
  - **SGID (`2xxx`, `rws` on group):** files created inside a shared directory inherit that directory's group.
  - **Sticky Bit (`1xxx`, `t` on others — e.g., `/tmp` is `1777` `drwxrwxrwt`):** everyone can write in `/tmp`, **only a file's owner (or `root`) can delete their own file**!
- **4. `$PATH` Rule:** Running `script.sh` fails if `.` isn't in `$PATH` (by design, for security) -> run `./script.sh`, move to `/usr/local/bin/`, or symlink with `ln -s`.
- **Try it:**
  ```bash
  scripts/sh.sh "ls -ld /tmp /usr/bin/passwd && umask"
  ```
- **Check Q:** Why does `/tmp` have permissions `drwxrwxrwt` (`1777`) instead of `0777`? — **A:** The Sticky Bit (`1` / `t`) prevents User A from deleting or renaming User B's temporary files inside a shared writable folder.

---

### U1.4 — Production Bash Scripting (Args, Functions, Loops, `trap` & `set -euo pipefail`)
- **Why it matters:** Moving from 5-line snippets to reliable automation requires defensive Bash habits.
- **5 Production Guardrails:**
  1. **`set -euo pipefail`:** exit on non-zero error (`-e`), fail on unset variables (`-u` — stops `rm -rf /$EMPTY/` disasters!), fail if any left stage of a pipe breaks (`-o pipefail`).
  2. **Always quote `"$var"` & `"$@"`:** preserves spaces (`my report.txt`) cleanly.
  3. **Positional Parameters & Functions:** `$1` first arg, `$#` arg count, `"$@"` all args; wrap reusable logic in `check_logs() { local file="$1"; ... }`.
  4. **Loops:** `for f in /workspace/training_lab/logs/*.log; do wc -l "$f"; done`.
  5. **`trap cleanup EXIT`:** guarantees temporary files or lockfiles get removed even when a script exits on error or Ctrl+C! Pairing with `set -x` traces commands during debugging.
- **Try it:**
  ```bash
  scripts/sh.sh "bash -c 'set -euo pipefail; cleanup() { rm -f /workspace/training_lab/tmp/trap_demo.tmp; }; trap cleanup EXIT; touch /workspace/training_lab/tmp/trap_demo.tmp; for f in /workspace/training_lab/logs/*.log; do printf \"%s -> %s lines\n\" \"\$f\" \"\$(wc -l < \"\$f\")\"; done'"
  ```
- **Check Q:** What does `trap cleanup EXIT` guarantee in an automation script? — **A:** It runs the `cleanup` function automatically whenever the script finishes, fails under `set -e`, or receives a termination signal, preventing stale lock/temp files.

---

## Self-Study Quiz Bank (For AI Quiz Mode)
1. Why can Linux report `"No space left on device"` when `df -h` still shows 40% free disk?
2. Contrast a hard link (`ln`) vs a symbolic link (`ln -s`) when the original file is deleted.
3. Explain what `SUID` (on `/usr/bin/passwd`) and the `Sticky Bit` (on `/tmp` `1777`) do.
4. Write an `awk` command to list hosts in `docs/servers.csv` where `cpu_pct >= 75`.
5. How does `umask 022` determine default permissions for new files vs new directories?
6. Why should `sed -i 's/\r$//'` be your first check when `bash: ./script.sh: /bin/bash^M: bad interpreter` appears?
7. What does each flag in `set -euo pipefail` protect against?
8. What is the difference between `type cd` and `which grep`?
