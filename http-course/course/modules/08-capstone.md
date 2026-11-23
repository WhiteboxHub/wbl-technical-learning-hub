# Module 8 — Capstone

Teach-skill content file. All demos run on the current stack. Verified live: all six fault injections (each shows its evidence and clears with `scripts/fix.sh`).
Time: about 2 hours.

## Objectives
Trace one request through every layer and name each HTTP concept used; diagnose six injected faults from evidence; deliver a small feature end to end.

## Stack requirements
`scripts/setup.sh` READY, then `scripts/fix.sh` once to reach the healthy baseline (monolith API + gateway + CORS on for the web page + auth off). For the trace in Beat 8.2 start auth: `docker compose -f docker-compose.yml -f docker-compose.cors.yml -f docker-compose.auth.yml up -d api`, then `TOKEN=$(scripts/token.sh hr_admin)`. The `departments-down` fault starts the split services itself (first run builds images; allow a minute).

---

### Beat 8.1 — The request we trace
- **Slides:** NEW slide: "One request, end to end" (the module table from the course outline)
- **Say:** `GET /v2/employees/5` from the HR portal in a browser, signed in through SSO, going through the gateway to the employees service, which calls the departments service and the database. Candidates will name every concept as it appears.
- **Ask:**
  - Q: Before we start, list as many layers as you can between the browser and the database. — A: Browser, DNS, TCP/TLS, gateway, auth, cache, service, other service, database.
- **Done when:** a layer list is on the board.

### Beat 8.2 — Trace it, layer by layer
- **Slides:** NEW slide(s): the trace table
- **Say:** work through the layers and name the concept and the earlier module: DNS/TCP/TLS (M1, M2), `fetch` and CORS preflight (M2), the access token in the `Authorization` header (M4, M5), gateway JWT validation and rate limit (M6), cache lookup (M6), role check on salary (M4), cross-service call with timeout and breaker (M7), JSON response with status, `Content-Type`, `ETag` (M1, M3).
- **Demo (run: agent):** one request, then its trail.
  ```bash
  curl -si -H "Authorization: Bearer $TOKEN" "http://localhost:8080/v2/employees/5?expand=department" | head -20
  docker compose logs --no-color --since 1m | grep "<x-request-id from the response>"
  ```
  **Point out:** the response headers show gateway, cache and request ID; the logs show the same ID in the gateway and both services.
- **Ask:**
  - Q: Where was authentication checked, and where was authorization checked? — A: Authentication at the gateway; authorization (salary, ownership) in the service.
  - Q: Which header proves it passed through the gateway? — A: `x-request-id` / `x-cache-status`.
- **Done when:** candidates can narrate the trace without the slide.

### Beat 8.3 — Break it, diagnose it
- **Slides:** none
- **Say:** the instructor injects one fault at a time; candidates diagnose from evidence (status, headers, logs) before anyone fixes it. Give the evidence first, not the cause.
- **Demo (run: agent):** for each fault, run it, let the room diagnose, then reveal and fix.
  ```bash
  scripts/break.sh expired-token     # evidence: 200, then {"detail":"token expired"} 401 a few seconds later
  scripts/break.sh wrong-role        # evidence: a manager asking for employee 1 gets 403 "you are not allowed to see this record"
  scripts/break.sh missing-cors      # evidence: the page on :3000 shows "Failed to fetch"; curl works; no access-control-allow-origin header
  scripts/break.sh rate-limit        # evidence: 200, 200, then 429 on ordinary routes through the gateway
  scripts/break.sh departments-down  # evidence: ~1 s per call three times, then fast; x-breaker: open; degraded department
  scripts/break.sh stale-cache       # evidence: x-cache-status HIT; /v2/departments returns 2 departments (database has 4); redis TTL ~3600
  scripts/fix.sh                     # clears everything
  ```
  Run one fault at a time, give the room the **evidence** (status codes, headers, timing, logs), let them diagnose, then reveal and run `scripts/fix.sh`.
  **Point out (answers, instructor only):** expired-token → token lifetime (JWT `exp`); wrong-role → authorization rule, not authentication (403 not 401); missing-cors → browser-only enforcement; rate-limit → gateway policy (`429`, `Retry-After`); departments-down → timeout, circuit breaker and fallback; stale-cache → a cache entry with a long TTL and no invalidation (`redis-cli DEL departments:list` fixes it).
- **Ask (per fault):**
  - Q: What did you see, which layer is responsible, and how do you confirm it? — A: See the comment on each fault.
- **Done when:** the room diagnoses at least four of six without hints.

### Beat 8.4 — Candidate project: leave requests
- **Slides:** NEW slide: the project brief
- **Say:** each candidate or pair adds a `leave-requests` feature end to end: endpoints designed with correct methods, status codes, pagination and errors (M3); employee creates and a manager approves (roles, M4); a route and a rate limit at the gateway (M6); a page that calls it, signed in via SSO (M2, M5); and a one-page written trace of one request.
- **Done when:** they know the deliverables and the rubric.

### Beat 8.5 — Wrap-up
- **Slides:** NEW slide: "What you can now do" and pointers
- **Say:** recap each module in one line. Pointers: GraphQL and gRPC, observability and tracing, Kubernetes, cloud API gateways, WebSockets, SAML, saga.
- **Ask:**
  - Q: Which module changed how you think about an API call? Why? — A: Open.
- **Done when:** the room has named one thing each.

---

## Rubric (for the project)
- Correct HTTP semantics and status codes
- Authentication and authorization applied correctly
- Error handling and documentation (OpenAPI)
- Reasoning about failure (timeouts, fallback)
- Clarity of the one-page request trace

## Done-check
1. Narrate the full trace unaided.
2. Diagnose at least four injected faults.
3. Submit the project against the rubric.

## Clean-up
`scripts/fix.sh`; `scripts/setup.sh --reset`.
