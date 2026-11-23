# Module 7 — Microservices

Teach-skill content file. All demos run on the current stack. Verified live: the split services through the gateway, the circuit breaker (timeouts, open, fail-fast, recovery), the `EmployeeHired` event on a Redis stream, and one request ID across all logs.
Time: about 90 minutes.

## Objectives
Explain monolith limits and when not to use microservices; split the HR system by bounded context; choose sync vs async communication; show a circuit breaker protecting a caller; explain CQRS and event sourcing at concept level; name what operating microservices requires.

## Stack requirements
Start the split architecture: `docker compose -f docker-compose.yml -f docker-compose.split.yml up -d --build`. The gateway (`http://localhost:8080`) then routes `/v2/employees*` to **employees-service** and `/v2/departments*` to **departments-service**, each with its **own database** (SQLite inside its container). employees-service calls departments-service with a **1 second timeout and a circuit breaker** (3 failures open it for 10 s, then one probe) and publishes `EmployeeHired` to the Redis stream `hr.events`. Every service logs the `X-Request-Id` and returns it. Use explicit `-f` flags in every `docker compose` command (the service names exist only with the split file). Go back with `scripts/fix.sh`. Beats 7.1, 7.2, 7.6 are slide-led.

---

### Beat 7.1 — Before microservices: the monolith
- **Slides:** 82–84
- **Say:** one deployable unit: UI, logic and data together. Strengths: simple to build, test, deploy, debug. Limits: scale everything together, slow releases, one tech stack, a bug can take down all of it.
- **Ask:**
  - Q: Give two strengths of a monolith. — A: Simple deployment, easy debugging, no network calls between modules.
  - Q: Give two limits. — A: Scaling as a unit, slow release cycles, tech lock-in, large blast radius.
- **Done when:** they can argue for a monolith.

### Beat 7.2 — What microservices are (and when not to use them)
- **Slides:** 85–90
- **Say:** small, independent, single-purpose services that own their data, deploy separately and talk over the network (Amazon, Netflix, eBay). Costs: network failures, distributed data, operational complexity. A small team with one product usually should stay monolithic.
- **Ask:**
  - Q: When should you not use microservices? — A: Small team, unclear domain, low scale.
- **Done when:** they can state one benefit and one cost.

### Beat 7.3 — Splitting the HR system: bounded contexts and DDD
- **Slides:** 95, 96 · NEW slide: "HR bounded contexts"
- **Say:** domain-driven design: bounded contexts, entities, value objects, aggregates, ubiquitous language. HR splits into employees, departments, leave, payroll. **Database per service**: no shared tables. Employees keeps only `department_id` and asks the departments service for names.
- **Demo (run: agent):** show the running pieces.
  ```bash
  docker compose -f docker-compose.yml -f docker-compose.split.yml ps --format "table {{.Service}}\t{{.Status}}\t{{.Ports}}"
  ```
  **Point out:** employees-service and departments-service are separate containers, each with its own database file (`employees.db`, `departments.db`). The old monolith `api` container is still running but the gateway no longer sends these paths to it.
- **Ask:**
  - Q: Why a database per service? — A: Independent change and deployment; shared tables couple services.
  - Q: What does employees store about a department? — A: Only the ID; the departments service owns the rest.
- **Done when:** they can draw the service boundaries.

### Beat 7.4 — Communication: sync vs async
- **Slides:** 101–104
- **Say:** synchronous (REST, gRPC): simple, immediate, but the caller waits and failures propagate. Asynchronous (queues, events: RabbitMQ, Kafka, Redis streams): decoupled and resilient, but eventual consistency and harder debugging. Use sync for queries that need an answer now, async for notifications and side effects.
- **Demo (run: agent):** a cross-service call.
  ```bash
  curl -si "http://localhost:8080/v2/employees/7?expand=department" | grep -iE "^HTTP|^x-served-by|^x-breaker|^x-request-id|^\{"
  ```
  **Point out:** one response, two services behind it: `x-served-by: employees-service`, a nested `department` object that came from departments-service, and `x-breaker: closed`.
- **Ask:**
  - Q: Sync or async: "send a welcome email after hire"? — A: Async.
  - Q: Sync or async: "show an employee with their department name"? — A: Sync.
- **Done when:** they can choose for three cases.

### Beat 7.5 — Resilience: timeouts, retries, circuit breaker
- **Slides:** 91 · NEW slide: "Timeouts, retries with backoff, circuit breaker, bulkhead, fallback"
- **Say:** every network call can fail or hang. Set timeouts, retry only idempotent calls with backoff, and use a circuit breaker: closed (normal) → open after repeated failures (fail fast) → half-open (probe) → closed. A fallback returns something useful (the department ID without a name).
- **Demo (run: agent):** make the dependency hang. (`pause` freezes the container so calls hang until the timeout; `stop` would make them fail instantly and hide the timeout lesson.)
  ```bash
  S="-f docker-compose.yml -f docker-compose.split.yml"
  docker compose $S pause departments-service
  for i in 1 2 3 4 5 6; do curl -s -o /tmp/b.json -D /tmp/h.txt -w "call $i: %{http_code} in %{time_total}s  breaker=" "http://localhost:8080/v2/employees/7?expand=department"; grep -i '^x-breaker' /tmp/h.txt | tr -d '\r' | cut -d' ' -f2; done
  python3 -c "import json; print(json.load(open('/tmp/b.json'))['department'])"
  docker compose $S unpause departments-service; sleep 11
  curl -s -o /dev/null -D /tmp/h.txt -w "after recovery: %{http_code} in %{time_total}s breaker=" "http://localhost:8080/v2/employees/7?expand=department"; grep -i '^x-breaker' /tmp/h.txt | tr -d '\r' | cut -d' ' -f2
  ```
  (zsh does not split `$S`; there, write the two `-f` flags out in each command.)
  **Point out (verified):** calls 1–3 take about **1 second** each (the timeout) yet still return `200` with a degraded fallback; the third failure **opens** the breaker; calls 4–6 take about **0.01 s** (fail fast) and return `{'id': 2, 'name': None, 'degraded': True, 'note': 'departments-service unavailable (circuit open, failing fast)'}`; after unpausing and waiting 10 s one probe goes through and the breaker returns to `closed`.
- **Ask:**
  - Q: Why fail fast when a dependency is down? — A: Stops requests piling up and exhausting the caller (cascading failure).
  - Q: Which calls are safe to retry? — A: Idempotent ones.
- **Done when:** they can describe closed, open and half-open.

### Beat 7.6 — Patterns: CQRS and event sourcing
- **Slides:** 93, 94, 97–100
- **Say:** CQRS separates writing (commands) from reading (queries) with different models. Event sourcing stores the sequence of events (`EmployeeHired`, `SalaryChanged`) and rebuilds state from them. Powerful for audit (HR!), but complex; use where history matters.
- **Ask:**
  - Q: One benefit of event sourcing in HR? — A: A full, auditable history of changes (e.g. every salary change).
  - Q: What does CQRS separate? — A: Reads from writes.
- **Done when:** they can explain the idea without the jargon.

### Beat 7.7 — Events and operating microservices
- **Slides:** NEW slide(s): "Containers, health checks, correlation ID, tracing; saga and eventual consistency"
- **Say:** containers and Compose give repeatable deployments; health checks tell the platform when to restart; a correlation ID ties logs together; tracing shows time per hop. No distributed transactions: use a saga (a chain of local transactions with compensations) and accept eventual consistency. Contract tests and per-service CI/CD keep teams independent.
- **Demo (run: agent):** publish an event, then follow one request through every log.
  ```bash
  S="-f docker-compose.yml -f docker-compose.split.yml"
  curl -s -o /dev/null -w "create: %{http_code}\n" -X POST http://localhost:8080/v2/employees -H 'Content-Type: application/json' \
    -d '{"name":"Event Demo","email":"event.demo@example.com","title":"Analyst","department_id":3,"manager_id":3,"hire_date":"2024-05-01","salary":80000}'
  docker compose exec -T redis redis-cli XRANGE hr.events - + COUNT 3
  RID=$(curl -si "http://localhost:8080/v2/employees/7?expand=department" | grep -i '^x-request-id' | tr -d '\r' | cut -d' ' -f2); echo "rid=$RID"
  docker compose $S logs --no-color --no-log-prefix employees-service departments-service gateway | grep "$RID"
  curl -s -o /dev/null -w "cleanup: %{http_code}\n" -X DELETE http://localhost:8080/v2/employees/21
  ```
  **Point out (verified):** the stream entry has `type EmployeeHired`, the employee id and the request id: employees-service published it without knowing who listens. The log search shows the same `rid=` in the gateway access log, employees-service and departments-service: one request, three places.
- **Ask:**
  - Q: Why a correlation ID? — A: To follow one request across many services' logs.
  - Q: Why can't you use one database transaction across services? — A: Each service owns its own database; use a saga and eventual consistency.
- **Done when:** they can find one request in two services' logs.

---

## Exercise (candidates, ~40 min)
Add a `leave-service` with its own database and `POST /v2/leave-requests`. Route it through the gateway, call employees to validate the employee, and publish `LeaveRequested`. Prove behavior when employees-service is down.

## Done-check
1. Argue for and against microservices for a small team.
2. Draw the HR bounded contexts and what each owns.
3. Choose sync or async for three cases.
4. Explain a circuit breaker's three states.
5. Find a request in two services' logs using a correlation ID.

## Clean-up
`scripts/fix.sh` (unpauses and returns to the monolith baseline); delete the `Event Demo` employee; `scripts/setup.sh --reset` for a fully clean database.
