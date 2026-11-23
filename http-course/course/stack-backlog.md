# Stack backlog

**Status: every component is built and verified.** Modules 1–8 demos all run on the current stack. See the table for what each component is and how it was checked.

All components below are built. If you add a new demo that needs a component that may be absent, tag it `needs: <ID>`; the teach skill probes for it and teaches from the slides when it is missing.

| ID | Component | Needed by | What to build |
|---|---|---|---|
| ~~WEB~~ **done** | HR directory page | M2 | Static page served on `http://localhost:3000` (nginx container, `web/`) that calls `GET /v2/employees` with `fetch` and lists employees. Includes buttons that write/read `localStorage`, `sessionStorage` and a cookie. |
| ~~CORS~~ **done** | CORS toggle | M2 | API reads `CORS_ORIGINS` env (empty = no CORS headers). `docker compose` override file `docker-compose.cors.yml` sets it to `http://localhost:3000`. |
| ~~COOKIE~~ **done** | Cookie demo endpoints | M2 | `GET /demo/cookie` sets a session cookie (`HttpOnly; SameSite=Lax`) and a plain cookie (`theme=dark; Max-Age=3600`); `GET /demo/whoami` echoes the cookies it received. |
| ~~EXTRAS~~ **done** | API extras | M3 | RFC 7807 `application/problem+json` errors (flag `PROBLEM_JSON=1`), `sort` and `q` query params on `/v2/employees`, `total` in a `X-Total-Count` header, `ETag` on `GET /v2/employees/{id}` with `If-Match` on PUT/PATCH (412), `Idempotency-Key` on `POST /v2/employees`. |
| ~~POSTMAN~~ **done** | Postman collection | M3 | `postman/hr.postman_collection.json` covering every endpoint, with a `base_url` variable. |
| ~~TESTS~~ **done** | pytest suite | M3 | `api/tests/` with a few tests; `docker compose run --rm api pytest`. |
| ~~AUTH~~ **done** | Authentication | M4 | `POST /v2/auth/token` (form: username, password) returns a signed JWT (claims `sub`, `role`, `dept`, `exp`); `Authorization: Bearer` required on `/v2/employees*` and `/v2/departments*` when `AUTH=1`; roles `hr_admin`, `manager`, `employee` with salary redaction rules (see Module 4); seed users in `api/app/seed_users.py` with dev-only passwords read from `DEMO_PASSWORD`; `GET /demo/basic` protected with HTTP Basic; short token lifetime configurable (`TOKEN_TTL`). |
| ~~KEYCLOAK~~ **done** | Identity provider | M5 | Keycloak container on `:8081`, realm `hr` imported from `keycloak/hr-realm.json` with users `hr_admin`, `manager`, `employee`, clients `portal`, `payroll`, `hr-api`. API validates tokens via the realm JWKS when `AUTH=oidc`. |
| ~~APPS~~ **done** | Two SSO demo apps | M5 | Tiny `portal` (`:3001`) and `payroll` (`:3002`) web apps using Keycloak login. |
| ~~VULN~~ **done** | Vulnerable demo app | M5 | `vuln/` service on `:3003` with a stored-XSS notes field, a CSRF-able delete, and a SQL-injectable search, plus fixed variants behind `?fixed=1`. |
| ~~GATEWAY~~ **done** | API gateway | M6, M7, M8 | nginx (or Traefik) on `:8080` in front of the API: routing, `X-Request-Id`, rate limit (5 req/min on a demo route, 429 + `Retry-After`), response cache with `X-Cache-Status`, `/v1` and `/v2` routing with `Deprecation`/`Sunset` on v1. |
| ~~REDIS~~ **done** | Redis | M6, M7 | Redis container used for cache and rate-limit counters, and an events stream. |
| ~~SPLIT~~ **done** | Split services | M7, M8 | `employees-service` and `departments-service` (own databases) behind the gateway; employees calls departments with a timeout and circuit breaker; publishes `EmployeeHired` to a Redis stream. |
| ~~FAULTS~~ **done** | Fault injector | M8 | `scripts/break.sh <fault>` and `scripts/fix.sh`: expired-token, wrong-role, missing-cors, rate-limit, departments-down, stale-cache. |

Suggested build order: ~~**WEB, CORS, COOKIE** (M2)~~ (done) → ~~**EXTRAS, POSTMAN, TESTS** (M3)~~ (done) → **AUTH** (M4) → **KEYCLOAK, APPS, VULN** (M5) → **GATEWAY, REDIS** (M6) → **SPLIT** (M7) → **FAULTS** (M8).

## How each was verified
| Component | Check |
|---|---|
| AUTH | 9 pytest tests; live 401/403/200 for 3 roles, tampered and expired tokens; Newman auth folder (8 assertions) |
| KEYCLOAK, APPS | real browser: PKCE login, SSO into the second app with no prompt, local vs IdP logout; Keycloak tokens accepted by the API (200/403/401) |
| VULN | XSS, SQL injection and CSRF exploits succeed on the vulnerable variant and are blocked on `?fixed=1` |
| GATEWAY, REDIS | request id header, 429 after 5 requests with `Retry-After`, cache MISS/HIT/invalidate, `/v1` deprecation headers, 401 at the edge |
| SPLIT | cross-service call, breaker (3 timeouts, open, fail fast, recovery), `EmployeeHired` on the stream, one request id in three logs |
| FAULTS | all six faults injected, evidence observed, cleared with `fix.sh` |

Not yet covered by automated tests: the web pages and the SSO apps (checked by hand in a browser).
