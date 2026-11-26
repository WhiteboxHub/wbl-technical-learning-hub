---
name: setup-candidate
description: Candidate (student) setup for the MySQL & Relational Databases course. Use when a candidate says "set up my environment", "I can't connect to MySQL", or needs to reset their practice database. Starts MySQL + Adminer + Redis with Docker and verifies their first SQL query.
---

# Candidate Setup — MySQL Course

Get a learner from a fresh laptop to their first working SQL query on `training_db`. Explain what each step does in one short sentence before running it.

## Steps

1. **Run `scripts/setup.sh`** from `mysql-course/`. Tell them the first run downloads Docker images and seeds 2,000+ rows, which takes 1–2 minutes.
2. **If it fails, handle the exit code:**
   - `10`: Docker missing -> share Docker Desktop link (`https://www.docker.com/products/docker-desktop/`). Do not install it for them.
   - `11`: Docker not running -> ask them to open Docker Desktop, wait for running status, then re-run.
   - `12`: Port `3306`, `8082`, or `6379` in use -> show what holds the port (e.g., an existing local MySQL install) and ask before stopping anything.
   - `13` / `14`: Check `docker compose logs mysql`, explain plainly, re-run.
   - `15`: `curl` missing -> explain how to install for their OS.
   On Windows, run `.sh` scripts via Git Bash or WSL2.
3. **First query together:**
   ```bash
   scripts/sql.sh "SELECT id, name, price FROM course;"
   ```
   Show the 6 courses and explain how to open Adminer (`http://localhost:8082`, Server `mysql`, User `root`, Pass `root`, DB `training_db`).
4. **Wrap up** with how to reset (`scripts/setup.sh --reset`), stop (`scripts/setup.sh --stop`), and start learning (`"start learning"` or `"quiz me"`).

## Rules
- Never fix errors silently; explain what broke.
- Do not edit `db/init/`, `db/solutions/`, or module files during setup.
- Only mention the dev-only local credentials (`root`/`root`) already in `docker-compose.yml`.
