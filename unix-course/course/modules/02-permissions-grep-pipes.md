# Module 2 — Permissions, `grep` & Unix Pipes (35 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **35 minutes** (`0:25–1:00`).
Deck slides: 26–30, 43–48 (plus pipes/redirection bridging Slide 3 & 8).
Story anchor: **The Workshop Badges & The Log Magnifying Glass** — every drawer in the workshop checks your ID badge (`u/g/o`) before letting you read, write, or execute; and when a server dumps thousands of log lines, you chain sharp filters (`grep | awk | sort | uniq`) instead of reading line by line.
Stack requirements: `scripts/setup.sh` READY.

## Objectives
Decode `ls -l` permission strings (`rwx` and octal `644`/`755`), fix `"Permission denied"` errors safely with `chmod`, search logs with `grep` and basic regex, and build multi-command pipelines with redirection.

---

### Beat 2.1 — File Ownership, Symbolic/Octal Permissions & `chmod` (12 min)
- **Slides:** 26–30
- **Say:**
  - `ls -l` prints a 10-character permission badge like **`-rwxr-xr--`**:
    - Character 1 = type (`-` regular file, `d` directory, `l` symlink).
    - Next 9 = three triples: **User (`u` / owner)**, **Group (`g`)**, **Others (`o` / everyone else)**.
  - **Octal math (base 8):** **`r = 4`, `w = 2`, `x = 1`**. Add them per triple:
    - **`644`** (`rw-r--r--`): normal text/config files (owner reads/writes, everyone else reads).
    - **`755`** (`rwxr-xr-x`): scripts, binaries, and directories (Note: for a **directory**, `x` means permission to `cd`/enter it!).
    - **`chmod -R`** applies recursively — never blindly run `chmod -R 777` in production (gives everyone write/execute access!).
  - **Ownership (`chown` & `chgrp`):** `sudo chown user:group file` changes owner and group (e.g., assigning app files to a service user); `chgrp group file` changes group only. Changing ownership of files you don't own requires `root` / `sudo`.
- **Demo (run: agent):** reproduce a real `"Permission denied"` error on `bin/onboarding_helper.sh` as `devuser`, inspect it, fix it with `chmod 755`, then restore cleanly.
  ```bash
  scripts/sh.sh "ls -l bin/onboarding_helper.sh && su -s /bin/bash devuser -c '/workspace/training_lab/bin/onboarding_helper.sh' 2>&1 || true"
  scripts/sh.sh "chmod 755 bin/onboarding_helper.sh && ls -l bin/onboarding_helper.sh && su -s /bin/bash devuser -c '/workspace/training_lab/bin/onboarding_helper.sh' && chmod 644 bin/onboarding_helper.sh"
  ```
  **Point out:** Same script content, zero code changes — only adding `x` (`644` -> `755`) turned `Permission denied` into a working run.
- **Candidate takeaway:** *"`r=4, w=2, x=1` across User/Group/Others; `644` fits data files, `755` fits executables/directories — never fix permission errors with `chmod 777`."*
- **Ask:**
  - Q: What permission string does `chmod 750 deploy.sh` produce? — A: `-rwxr-x---` (owner rwx = 7, group r-x = 5, others --- = 0).
- **Done when:** candidates convert between symbolic (`rwxr-xr-x`) and octal (`755`) in their head.

### Beat 2.2 — `grep` & Regular Expressions (13 min)
- **Slides:** 43–48
- **Say:**
  - Servers don't have GUIs or Ctrl+F — `grep` (*Global Regular Expression Print*) is how engineers find needles in multi-million-line logs at 2 a.m.
  - **Essential flags (`grep [options] pattern [file...]`):**
    - **`-i`** case-insensitive, **`-v`** invert (exclude lines!), **`-n`** show line numbers, **`-r`/`-R`** recursive directory search, **`-l`** filenames only, **`-c`** count matching lines, **`-E`** extended regex (replaces deprecated `egrep`), **`-F`** fixed literal string — much faster (replaces deprecated `fgrep`).
  - **Essential Regex anchors:** `^start` (line begins with), `end$` (line ends with), `^exact$`, `[0-9]` (digit class), `.*` (any characters). Always quote regex patterns in the shell (`'...'`) so Bash doesn't interpret `*` or `$`!
- **Demo (run: agent):** query `logs/app.log` (`120` lines) and `logs/auth.log` (`30` lines) with counts, line numbers, inverted match, and regex.
  ```bash
  scripts/sh.sh "wc -l logs/app.log && grep -c 'ERROR' logs/app.log && grep -cE 'ERROR|FATAL' logs/app.log"
  scripts/sh.sh "grep -n 'FATAL' logs/app.log | head -n 3"
  scripts/sh.sh "grep -rn 'PORT' config/"
  ```
  **Point out:** `app.log` has `120` total lines, `15` `ERROR` lines, and `20` `ERROR|FATAL` lines (`-cE` matches both without spawning two greps).
- **Candidate takeaway:** *"Quote patterns cleanly and remember the high-signal `grep` flags: `-i` case, `-v` exclude, `-n` line number, `-c` count, `-r` recursive, `-E` regex, `-F` fast literal."*
- **Ask:**
  - Q: Why use `grep -F '10.0.1.5'` instead of plain `grep '10.0.1.5'` when searching a 2 GB log for an exact string? — A: `-F` skips regex parsing (and stops `.` from acting as a wildcard), making fixed-string search faster and exact.
- **Done when:** candidates predict whether a `grep` flag counts, inverts, or searches recursively.

### Beat 2.3 — Pipes (`|`) & Stream Redirection (`>`, `>>`, `2>`) (10 min)
- **Slides:** 3, 7–8, 48
- **Say:**
  - Remember **"Tools, not towers"**: every Unix command has **3 standard streams**: **stdin (`0`)**, **stdout (`1`)**, **stderr (`2`)**.
  - **Pipe (`|`):** connects stdout of the left command directly into stdin of the right command (no temp file needed!).
    - Classic production incident chain: `grep ... | awk ... | sort | uniq -c | sort -nr`
  - **Redirection:** **`>`** overwrites a file, **`>>`** appends to a file, **`2>`** redirects errors, **`> file 2>&1`** captures both stdout & errors (or `&>` in Bash). Need to save output AND watch it on screen? Use **`tee`** (`... | tee out.log`).
- **Demo (run: agent):** rank the offending IPs in `logs/auth.log` (`8` failed logins) in one pipeline, and save a filtered slice with `>`.
  ```bash
  scripts/sh.sh "grep -c 'Failed password' logs/auth.log && grep 'Failed password' logs/auth.log | awk '{print \$(NF-3)}' | sort | uniq -c | sort -nr"
  scripts/sh.sh "grep 'FATAL' logs/app.log > tmp/fatal_demo.log && wc -l tmp/fatal_demo.log && rm -f tmp/fatal_demo.log"
  ```
  **Point out:** Notice how `sort` MUST run before `uniq -c` (`uniq` only collapses **adjacent** duplicate lines!). Also warn: `>` overwrites without asking!
- **Candidate takeaway:** *"`|` passes stdout to the next tool cleanly; `>` overwrites while `>>` appends; always `sort` before `uniq -c`."*
- **Ask:**
  - Q: Why does `cat access.log | uniq -c` fail to count total hits per IP unless you put `sort` in between? — A: `uniq` only deduplicates adjacent identical lines; sorting groups identical lines together first.
- **Done when:** candidates build a 3-stage pipe and distinguish `>` from `>>`.

---

## Post-Class Practice (Candidates)
Complete [labs/module-02-permissions-grep-pipes.sh](../../labs/module-02-permissions-grep-pipes.sh) (~20 min after class; predict counts first!).
