---
name: setup-docker-class
description: Pre-flight check and one-command stack startup for the Docker ("The Shipping Container") course. Use when the instructor says "set up the class", "setup docker class", "verify setup", or "start the stack". Verifies Docker Engine/Desktop, Compose v2, modules, API, and runs scripts/setup.sh.
---

# Setup Docker Class

You are preparing the live classroom environment for **Docker — Images, Containers, Dockerfile, Volumes, Networking & Containerising the Python API** (Story Anchor: **The Shipping Container**).

## Steps
1. **Verify Repository Assets**:
   - All 5 module files exist under `course/modules/01-*.md` to `05-*.md`.
   - `api/Dockerfile`, `api/.dockerignore`, `api/app/main.py`, `api/app/database.py`, `api/app/schemas.py`, `api/tests/test_main.py`, `docker-compose.yml`, `scripts/setup.sh`, `scripts/smoke.sh`, `scripts/break.sh`, and `scripts/fix.sh` exist.
   - All 4 skills in `.claude/skills/` (`setup-docker-class`, `teach-docker-class`, `practice-docker`, `setup-candidate`) exist.
2. **Run Live Stack Check**:
   - Run `./scripts/setup.sh` in the terminal.
   - Translate exit codes into plain English if it fails:
     - `10`: Docker or Compose v2 is not installed.
     - `11`: Docker Desktop is not running — ask the instructor to start Docker Desktop and wait for the whale icon to settle.
     - `12`: Port `8000` is in use (often `http-course` API is still running) — offer to inspect with `lsof -i :8000` or `docker ps`.
     - `13` / `14`: Show the last 20 lines of `docker compose logs api` and diagnose.
3. **Run Containerised Unit Tests**:
   - Run `docker compose exec api pytest -q` and confirm all tests pass.
4. **Report Readiness**:
   - Print `STATUS: READY TO TEACH` and prompt: `Type "teach module 1" to begin.`
   - Note: Never run `--reset` (`docker compose down -v`) without explicit confirmation.
