---
name: setup-candidate
description: Candidate (student) setup for the Unix & Shell Scripting Essentials course. Use when a candidate says "set up my environment", "docker unix lab isn't starting", or needs to reset their workspace. Builds and starts the Ubuntu 24.04 Unix Lab container and verifies their first shell command.
---

# Candidate Setup — Unix Course

Get a learner from a fresh laptop to their first working Linux command in `/workspace/training_lab`. Explain what each step does in one short sentence before running it.

## Steps

1. **Run `scripts/setup.sh`** from `unix-course/`. Tell them the first run builds a small Ubuntu 24.04 Docker container (~1–2 minutes).
2. **If it fails, handle the exit code:**
   - `10`: Docker missing -> share Docker Desktop link (`https://www.docker.com/products/docker-desktop/`). Do not install it for them.
   - `11`: Docker not running -> ask them to open Docker Desktop, wait for running status, then re-run.
   - `12`: Port `8085` in use -> show what holds port `8085` and ask before stopping anything.
   - `13` / `14`: Check `docker compose logs unix`, explain plainly, re-run.
   - `15`: `curl` missing -> explain how to install for their OS.
   On Windows, run `.sh` scripts via Git Bash or WSL2.
3. **First command together:**
   ```bash
   scripts/sh.sh "pwd && ls -la docs/ && grep -c 'ERROR' logs/app.log"
   ```
   Show the `docs/` files (`Report.txt` vs `report.txt`) and `15` ERROR lines in `logs/app.log`.
4. **Wrap up** with how to open an interactive Linux shell (`scripts/sh.sh`), reset (`scripts/setup.sh --reset`), stop (`scripts/setup.sh --stop`), and start learning (`"start learning"` or `"quiz me"`).

## Rules
- Never fix errors silently; explain what broke.
- Do not edit `docker/`, `solutions/`, or module files during setup.
