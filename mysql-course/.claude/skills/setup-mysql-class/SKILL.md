---
name: setup-mysql-class
description: Instructor setup for the MySQL & Relational Databases course. Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or the MySQL stack is not running. Checks Docker, starts MySQL 8.0 + Adminer + Redis, runs the smoke test, and reports readiness.
---

# Instructor Setup — MySQL Course

Gets the instructor's machine ready to teach using `scripts/setup.sh`.

## Steps

1. **Run the setup script** from `mysql-course/`: `scripts/setup.sh`. First run downloads `mysql:8.0`, `adminer:4`, and `redis:7-alpine` images and seeds 2,000+ rows.
2. **Handle the exit code:**

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Go to step 3 |
| 10 | Docker missing | Tell the instructor to install Docker Desktop (link in script output). Do not install it for them. |
| 11 | Docker not running | Ask them to start Docker Desktop and wait until it says running, then re-run. |
| 12 | Port 3306, 8082, or 6379 in use | Show which program holds the port. Ask before stopping anything. |
| 13 | MySQL unhealthy | Read `docker compose logs mysql`, explain the cause, fix repo issues if any, re-run. |
| 14 | Smoke test failed | Show the FAIL lines, check seed state (`scripts/setup.sh --reset` only with approval). |
| 15 | curl missing | Ask them to install curl. |

3. **Check the teaching environment:**
   - `docs/course-toc.md` and `course/modules/` exist
   - MySQL responds: `scripts/sql.sh "SELECT COUNT(*) FROM student;"` returns `8`
   - Adminer loads: `curl -sI http://localhost:8082` returns `200`
   - Redis responds: `docker compose exec -T redis redis-cli PING` returns `PONG`
4. **Report a short readiness checklist** with connection details (`localhost:3306`, DB `training_db`, user `root`, pass `root`), Adminer URL (`http://localhost:8082`), reset (`scripts/setup.sh --reset`), and stop (`scripts/setup.sh --stop`).
5. **Point to the next step:** say `teach class` (for the full 2-hour session) or `teach module 1` (through `teach module 4`).

## Rules
- Idempotent: safe to re-run on an already healthy stack.
- Never run `--reset` (wipes volume) without asking the instructor first.
- Credentials in `docker-compose.yml` (`root` / `root`) are dev-only for local classroom use.
