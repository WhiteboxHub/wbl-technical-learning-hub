---
name: setup-unix-class
description: Instructor setup for the Unix & Shell Scripting Essentials course. Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or the wbl-unix container is not running. Checks Docker, starts the Ubuntu 24.04 Unix Lab container, seeds /workspace/training_lab, runs smoke test, and reports readiness.
---

# Instructor Setup — Unix Course

Gets the instructor's machine ready to teach using `scripts/setup.sh`.

## Steps

1. **Run the setup script** from `unix-course/`: `scripts/setup.sh`. First run builds `wbl-unix-lab:ubuntu-24.04` and seeds `/workspace/training_lab`.
2. **Handle the exit code:**

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Go to step 3 |
| 10 | Docker missing | Tell the instructor to install Docker Desktop (link in script output). Do not install it for them. |
| 11 | Docker not running | Ask them to start Docker Desktop and wait until it says running, then re-run. |
| 12 | Port 8085 in use | Show which program holds port 8085. Ask before stopping anything. |
| 13 | Container unhealthy | Read `docker compose logs unix`, explain the cause, fix repo issues if any, re-run. |
| 14 | Smoke test failed | Show the FAIL lines, check workspace seed (`scripts/setup.sh --reset` only with approval). |
| 15 | curl missing | Ask them to install curl. |

3. **Check the teaching environment:**
   - `docs/course-toc.md` and `course/modules/` exist
   - Linux responds: `scripts/sh.sh "uname -s && wc -l < logs/app.log"` returns `Linux` and `120`
   - HTTP listener loads: `curl -sI http://localhost:8085/readme.txt` returns `200`
4. **Report a short readiness checklist** with `scripts/sh.sh` usage, seeded counts (`120` lines in `logs/app.log`, `30` lines in `logs/auth.log`), lab HTTP URL (`http://localhost:8085/readme.txt`), reset (`scripts/setup.sh --reset`), and stop (`scripts/setup.sh --stop`).
5. **Point to the next step:** say `teach class` (for the full 2-hour session) or `teach module 1` (through `teach module 4`).

## Rules
- Idempotent: safe to re-run on an already healthy container.
- Never run `--reset` (wipes volume) without asking the instructor first.
- Credentials (`devuser` / `devpass`) are dev-only inside the local container.
