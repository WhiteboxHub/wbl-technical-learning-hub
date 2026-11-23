---
name: setup-http-class
description: Instructor setup for the HTTP/APIs/Auth/Microservices course. Use when an instructor wants to prepare their machine for teaching, says "set up the class", "get ready to teach", or the demo stack is not running. Checks prerequisites, starts the HR stack with Docker Compose, runs the smoke test, and reports readiness.
---

# Instructor setup

Gets the instructor's machine ready to teach. The work is done by `scripts/setup.sh`; your job is to run it, interpret the result, and fix what you safely can.

## Steps

1. **Run the setup script** from the repo root: `scripts/setup.sh`. First run downloads images and can take several minutes; run it in the background if needed and report progress.
2. **Handle the exit code:**

| Exit | Meaning | What to do |
|---|---|---|
| 0 | Ready | Go to step 3 |
| 10 | Docker missing | Tell the instructor to install Docker Desktop (link in the script output). Do not install it for them. |
| 11 | Docker not running | On macOS, ask before running `open -a Docker`, then wait up to ~2 minutes for `docker info` to succeed and re-run. On other systems, ask them to start Docker. |
| 12 | Port 8000 or 5432 in use | Show which program holds the port. Ask before stopping anything. Never kill a process without the instructor's approval. |
| 13 | API unhealthy | Read `docker compose logs api db`, explain the cause, fix if it is in this repo, re-run. |
| 14 | Smoke test failed | Show the FAIL lines, investigate against `api/app/main.py`, re-run. |
| 15 | curl missing | Ask them to install curl. |

3. **Check the teaching environment** (report each as ready or missing; do not invent missing items):
   - `docs/course-toc.md` exists
   - `http-course` demo requests work: `curl -s localhost:8000/v2/employees/1`
   - Swagger UI loads: `curl -sI localhost:8000/docs` returns 200
   - Tools to demo with: `curl --version`, and whether Postman is installed (optional; suggest it, do not install it)
   - Browser available for DevTools demos
4. **Report a short readiness checklist**, with URLs (API, Swagger, Postgres), and how to reset (`scripts/setup.sh --reset`) and stop (`scripts/setup.sh --stop`).
5. **Point to the next step:** the instructor starts a class with the teach skill (once it exists for the module they want). Today only setup is available, so say so plainly.

## Rules
- Idempotent: running again on a healthy stack is safe and quick.
- `--reset` wipes the database volume. Only use it if the instructor asks, or demo data was changed and they want seed data back.
- Do not modify `docker-compose.yml` or application code just to get setup to pass without telling the instructor what and why.
- Never print or invent credentials. The only credentials are the dev-only ones in `docker-compose.yml`, which are fine to mention for the local Postgres.
