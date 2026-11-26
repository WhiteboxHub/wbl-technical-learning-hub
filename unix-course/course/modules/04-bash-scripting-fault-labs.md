# Module 4 — Bash Scripting, Exit Codes & Live Fault Triage (30 min)

Teach-skill & AI-tutor content file.
Time budget in 2-hour class: **30 minutes** (`1:30–2:00`).
Deck slides: 49–62 (+ live fault diagnosis; Cron deep dive sits in post-class Self-Study 2 so live class stays on time).
Story anchor: **The Repeatable Recipe Card & The Incident Shift** — typing 10 commands by hand works once; turning them into a `.sh` recipe with a shebang (`#!/bin/bash`), `+x` badge, conditionals, and exit codes lets a server verify itself reliably — and handle failures calmly.
Stack requirements: `scripts/setup.sh` READY; `scripts/fix.sh` clean baseline.

## Objectives
Write an executable Bash script (`#!/bin/bash`, variables, numeric comparisons, `if/elif/else/fi`), inspect exit codes (`$?`), chain error handling with `&&` / `||`, and diagnose 2 live Unix faults using `scripts/break.sh`.

---

### Beat 4.1 — Bash Shell, Shebang (`#!`), Variables & Math (10 min)
- **Slides:** 49–58, 61 *(skip writing complex cron schedules live — covered in Self-Study 2)*
- **Say:**
  - **Bash startup:** interactive terminals read **`~/.bashrc`** / **`~/.bash_profile`** (`$` prompt for users, `#` for `root`).
  - **2 rules for standalone scripts:**
    1. **Line 1 must be the Shebang:** `#!/bin/bash` (or `#!/usr/bin/env bash`). Tells the kernel which interpreter runs the file (the `.sh` extension is just convention!).
    2. **Executable permission:** `chmod +x script.sh`, then run `./script.sh`.
  - **Variables & Input (NO spaces around `=`!):** `name="WBL"`, print with `"$name"`, read interactively with `read -p "Prompt: " var`.
  - **Arithmetic inside `$(( ... ))`:** `+`, `-`, `*` (multiplication), `/` (integer division), `**` (exponentiation), `%` (modulo). *(Slide clarification: Slide 58's screenshot dropped `*` on multiplication and printed `*` on exponentiation — in Bash, `*` multiplies and `**` raises to a power.)*
- **Demo (run: agent):** build and run a tiny Bash check script inside `tmp/`, then verify exit status and clean up.
  ```bash
  scripts/sh.sh "cat > tmp/demo.sh <<'EOF'
#!/usr/bin/env bash
count=\$(grep -c 'ERROR' /workspace/training_lab/logs/app.log)
doubled=\$((count * 2))
echo \"Errors=\$count Doubled=\$doubled\"
EOF
chmod +x tmp/demo.sh && ./tmp/demo.sh && rm -f tmp/demo.sh"
  ```
  **Point out:** Zero spaces around `count=` and `doubled=`; `$((count * 2))` evaluates arithmetic directly.
- **Candidate takeaway:** *"Start every script with `#!/usr/bin/env bash`, assign variables without spaces around `=`, quote expansions (`"$var"`), and grant `chmod +x`."*
- **Ask:**
  - Q: Why does `name = "WBL"` fail in Bash while `name="WBL"` works? — A: With spaces, Bash treats `name` as a command name and `=` as its first argument; variable assignment requires no spaces around `=`.
- **Done when:** candidates write a 3-line Bash script with a shebang, variable, and `chmod +x`.

### Beat 4.2 — Numeric Comparisons, `if/elif/else`, Exit Codes & `&&`/`||` (10 min)
- **Slides:** 59–62
- **Say:**
  - **6 Numeric Operators inside `[ ... ]` (not `<` or `>`!):**
    - **`-eq`** equal, **`-ne`** not equal, **`-gt`** greater than, **`-ge`** `>=`, **`-lt`** less than, **`-le`** `<=`.
    - *(Why not `>` in `[ ... ]`? Because `>` redirects stdout to a file!)*
  - **Conditionals:** `if [ ... ]; then ... elif [ ... ]; then ... else ... fi` (`fi` closes `if`).
  - **Exit Codes (`$?`):** Every command returns `0` for **success**, or `1–255` for **failure**. Explicitly return status with `exit 0` or `exit 1`.
  - **Short-circuit error handling:**
    - `cmd1 && cmd2` -> run `cmd2` **only if** `cmd1` succeeds (`exit 0`).
    - `cmd1 || cmd2` -> run `cmd2` **only if** `cmd1` fails (`exit != 0`).
- **Demo (run: agent):** compare `app.log` error count (`15`) against a threshold (`10`), check `$?`, and show `&&` vs `||`.
  ```bash
  scripts/sh.sh "err=\$(grep -c 'ERROR' logs/app.log); if [ \"\$err\" -gt 10 ]; then echo \"ALERT: \$err errors\"; else echo \"OK\"; fi"
  scripts/sh.sh "./bin/healthcheck.sh && echo 'healthcheck passed (exit=0)'; ls /no_such_file 2>/dev/null || echo 'caught missing file with ||'"
  ```
  **Point out:** `ls /no_such_file` returned non-zero so `||` caught it immediately instead of silently ignoring failure.
- **Candidate takeaway:** *"In `[ ... ]` compare numbers with `-eq/-ne/-gt/-lt`; inspect `$?` (`0` = ok, non-zero = error); wire `&&` for on-success and `||` for fallback."*
- **Ask:**
  - Q: Inside `[ "$err" -gt 10 ]`, what happens if you accidentally write `[ "$err" > 10 ]`? — A: Single `[` treats `>` as output redirection and creates an unwanted file named `10` instead of comparing numbers.
- **Done when:** candidates read `$?` and explain `-gt`, `&&`, and `||`.

### Beat 4.3 — Live Fault Triage (`scripts/break.sh`) + Capstone Handoff (10 min)
- **Slides:** Synthesis of 1–62
- **Say:**
  - Time to test everything from Modules 1–4 as an on-call engineer: never guess — **observe -> isolate -> fix -> verify**.
- **Demo (run: agent — pick 2 faults live, always finish with `scripts/fix.sh`):**
  ```bash
  # Fault 1: bad-perms
  scripts/break.sh bad-perms
  scripts/sh.sh "./bin/backup.sh 2>&1; echo exit_code=\$?"
  scripts/sh.sh "ls -l bin/backup.sh"

  # Fault 2: runaway-proc (plus quick log & socket health verify)
  scripts/break.sh runaway-proc
  scripts/sh.sh "ps aux | grep wbl_runaway_worker | grep -v grep && ss -tuln | grep 8080 && grep -c 'FATAL' logs/app.log"

  # Clean restore
  scripts/fix.sh
  scripts/sh.sh "./bin/backup.sh && echo backup_ok"
  ```
  **Point out:** Fault 1 showed `Permission denied` + `ls -l` `-rw-r--r--` (`644` missing `+x`). Fault 2 showed a live worker PID ready for `kill` / `pkill`. `scripts/fix.sh` restores everything cleanly.
- **Post-Class Capstone Assignment:**
  - Assign [labs/module-04-bash-scripting-capstone.sh](../../labs/module-04-bash-scripting-capstone.sh) (`check_threshold.sh` + `server_audit.sh` over `docs/servers.csv`) and point candidates to [course/self-study/](../self-study/01-unix-daily-engineering-toolkit.md) for post-class deep dives + the 8-question AI quiz.
- **Done when:** candidates diagnose both live faults from terminal evidence before touching `fix.sh`.
