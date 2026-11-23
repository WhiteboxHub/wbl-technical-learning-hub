# HTTP, APIs, Auth and Microservices — Course Repo

Running example: an HR system (employees, departments, managers).

## Guides
- [Class-day quick start](docs/class-day-quickstart.md) — 5-minute instructor checklist
- [Instructor Guide](docs/instructor-guide.md) — setup, running a class with the agent, Module 1 plan, troubleshooting
- [Student Guide](docs/student-guide.md) — laptop setup, HR API reference, Module 1 cheat sheet and exercise

## Start the stack
Requires Docker Desktop running.

```bash
docker compose up --build -d
scripts/smoke.sh
```

- API: http://localhost:8000/v2/employees
- Directory page: http://localhost:3000 (Module 2)
- Gateway: http://localhost:8080 (Module 6) · Redis `:6379`
- Vulnerable demo app: http://localhost:3003 (Module 5, intentionally insecure; never deploy)
- Optional SSO stack: `docker compose --profile sso up -d --build` → Keycloak :8081, portal :3001, payroll :3002
- Swagger UI: http://localhost:8000/docs
- Postgres: `localhost:5432` (user `hr`, db `hr`; dev-only password in `docker-compose.yml`)

Run the API tests: `docker compose run --rm api pytest -q`

Reset to seed data: `docker compose down -v && docker compose up --build -d`

## Endpoints (v2)
| Method | Path | Notes |
|---|---|---|
| GET | `/health` | liveness |
| GET | `/demo/cookie`, `/demo/whoami` | Module 2 cookie demo |
| GET/POST | `/v2/departments` | list, create (201 + `Location`) |
| GET/PUT/DELETE | `/v2/departments/{id}` | delete returns 409 if employees remain |
| GET | `/v2/departments/{id}/employees` | nested route |
| GET/POST | `/v2/employees` | `?limit=&offset=&department_id=&q=&sort=` ; `X-Total-Count` header ; POST honors `Idempotency-Key` |
| GET/PUT/PATCH/DELETE | `/v2/employees/{id}` | GET returns `ETag` (`If-None-Match` → 304); PUT/PATCH honor `If-Match` (412) |

Seed: 4 departments, 20 employees with a manager hierarchy.

## Layout
```
docker-compose.yml   db + api + web (:3000)
docker-compose.cors.yml  override: CORS on for the web page (Module 2)
docker-compose.problem.yml  override: RFC 7807 problem+json errors (Module 3)
docker-compose.auth.yml / .oidc.yml  overrides: JWT auth (Module 4) / Keycloak tokens (Module 5)
docker-compose.split.yml  override: employees + departments services (Module 7)
gateway/             nginx gateway configs (Modules 6-7)
keycloak/ sso-app/ vuln/ services/   Module 5 and 7 components
scripts/token.sh, jwt-decode.py, break.sh, fix.sh   helpers for Modules 4 and 8
postman/             Postman collection for the HR API (Module 3)
web/                 HR directory page (static)
api/                 FastAPI app (app/main.py, models, schemas, seed) + tests/ (pytest -q)
scripts/setup.sh     prerequisite checks + start + smoke test (--reset, --stop)
scripts/smoke.sh     status-code checks, called by setup.sh
.claude/skills/      setup-http-class, teach-http-class (instructors); setup-candidate, practice-http (candidates)
docs/                course table of contents
```
