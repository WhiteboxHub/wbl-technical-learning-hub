# Module 3 — JSON and REST APIs

Teach-skill content file. All demos run on the current stack (verified: curl commands, 8 pytest tests, and the 30-request Postman collection run in Newman with 0 failures).
Time: about 2 sessions (split after Beat 3.5 if time is short). Biggest module.

## Objectives
Write and validate JSON; explain REST and design endpoints; do full CRUD with the right methods and status codes; handle errors, pagination, filtering and docs; know the advanced patterns (ETag, idempotency keys, async, webhooks).

## Stack requirements
`scripts/setup.sh` READY. Postman collection: `postman/hr.postman_collection.json` (variable `base_url` = `http://localhost:8000`). For Beat 3.6 the problem+json override is `docker-compose.problem.yml`; run `docker compose up -d` afterwards to return to default errors. Idempotency keys are remembered in API memory, so a restart (reset) forgets them.

---

### Beat 3.1 — JSON
- **Slides:** 105–117 (reordered to the front; fix the "SOAP" wording on slide 107)
- **Say:**
  - JSON is text: objects `{}`, arrays `[]`, strings (double quotes only), numbers, booleans, `null`. No comments, no trailing commas.
  - Smaller and easier than XML for APIs; never parse with `eval`.
  - A schema describes the shape: JSON Schema → in our app, a Pydantic model → published as OpenAPI.
- **Demo (run: agent):**
  ```bash
  curl -s http://localhost:8000/v2/employees/1 | python3 -m json.tool
  curl -s -X POST http://localhost:8000/v2/departments -H 'Content-Type: application/json' -d '{bad json' | python3 -m json.tool
  curl -s http://localhost:8000/openapi.json | python3 -c "import sys,json; print(json.dumps(json.load(sys.stdin)['components']['schemas']['EmployeeIn'], indent=2))"
  ```
  **Point out:** a nested-free employee object; broken JSON is rejected with a JSON-parse error (422); the schema lists required fields, types and constraints, generated from the model.
- **Ask:**
  - Q: Two things valid JavaScript objects allow that JSON does not? — A: Single quotes or unquoted keys, trailing commas, comments.
  - Q: Why never `eval` a JSON string? — A: It executes arbitrary code.
  - Q: What does `required` do in a schema? — A: The field must be present.
- **Done when:** they can spot three JSON syntax errors.

### Beat 3.2 — Web service, API, REST
- **Slides:** 20–24, 26, 29–32 (swap the weather example for HR; drop the SOAP slides)
- **Say:**
  - A web service is machine-to-machine communication over a network. An API is the contract. REST is a style: resources, a uniform interface, stateless, cacheable, client-server, layered.
  - Maturity model: level 0 one endpoint, 1 resources, 2 methods + status codes (where most real APIs live), 3 hypermedia links.
- **Ask:**
  - Q: "Stateless" in REST? — A: Each request carries all the context the server needs.
  - Q: Is an HTTP API automatically RESTful? — A: No; REST is a set of constraints.
- **Done when:** they can define resource and representation.

### Beat 3.3 — Endpoint design
- **Slides:** 57 · NEW slide: "Good and bad endpoints"
- **Say:** nouns not verbs, plural collections, nesting for relationships, lowercase, hyphens. Bad: `/getEmployee`, `/employees/delete/5`. Good: `GET /employees/5`, `GET /departments/2/employees`.
- **Demo (run: agent):** list every route the API actually exposes.
  ```bash
  curl -s http://localhost:8000/openapi.json | python3 -c "import sys,json; [print(m.upper().ljust(7), p) for p,v in json.load(sys.stdin)['paths'].items() for m in v]"
  ```
  **Point out:** collection vs item routes, one nested route, methods carry the verbs.
- **Ask:**
  - Q: Rewrite `POST /createEmployee` as REST. — A: `POST /employees`.
  - Q: Path or query for "employees in Engineering"? — A: `/departments/2/employees` or `/employees?department_id=2`.
- **Done when:** they can fix three bad endpoints.

### Beat 3.4 — CRUD with methods
- **Slides:** 33–56 (students → employees)
- **Say:** Create POST (201 + `Location`), Read GET (200/404), Replace PUT (200), Partial update PATCH (200), Delete DELETE (204).
- **Demo (run: instructor):** import `postman/hr.postman_collection.json` into Postman and run folder **1 Employees CRUD** request by request, in order: create (saves `emp_id`), read (saves the `ETag`), PUT, PATCH, DELETE, read again (404). Each request has a built-in test that turns green. Then show the **Run collection** button.
- **Demo (run: agent):** the same lifecycle with `curl`, as in Beat 1.5 but on departments:
  ```bash
  curl -si -X POST http://localhost:8000/v2/departments -H 'Content-Type: application/json' -d '{"name":"Legal","location":"Austin"}'
  curl -s  http://localhost:8000/v2/departments/$ID
  curl -si -X PUT http://localhost:8000/v2/departments/$ID -H 'Content-Type: application/json' -d '{"name":"Legal & Compliance","location":"Austin"}'
  curl -si -X DELETE http://localhost:8000/v2/departments/$ID
  ```
  Take `ID` from the `location` header of the POST. **Point out:** 201 + `location`, 200 with the full object, 204 with no body.
- **Ask:**
  - Q: What should POST return? — A: 201, the new resource, and its URL in `Location`.
  - Q: What should the server do if a PUT targets a missing ID? — A: 404 (or create it, if the API chooses upsert).
- **Done when:** every candidate has made one create-read-update-delete cycle.

### Beat 3.5 — PUT vs POST, idempotency, retries
- **Slides:** 48–54 (trim to 2)
- **Say:** POST creates and is not idempotent; PUT replaces and is. Networks retry, so a repeated POST can create duplicates unless the server dedupes with an `Idempotency-Key`.
- **Demo (run: agent):**
  ```bash
  B=http://localhost:8000
  curl -s -o /dev/null -w "PUT 1: %{http_code}\n" -X PUT $B/v2/departments/4 -H 'Content-Type: application/json' -d '{"name":"Sales","location":"Austin"}'
  curl -s -o /dev/null -w "PUT 2: %{http_code}\n" -X PUT $B/v2/departments/4 -H 'Content-Type: application/json' -d '{"name":"Sales","location":"Austin"}'
  curl -s -o /dev/null -w "POST 1: %{http_code}\n" -X POST $B/v2/departments -H 'Content-Type: application/json' -d '{"name":"Ops","location":"Austin"}'
  curl -s -o /dev/null -w "POST 2: %{http_code}\n" -X POST $B/v2/departments -H 'Content-Type: application/json' -d '{"name":"Ops","location":"Austin"}'
  ```
  **Point out:** identical PUTs give identical results. The second POST here is rejected (409) only because department names are unique; without that constraint it would create a duplicate.
  Clean up: delete the `Ops` department the demo created.
- **Demo (run: agent):** the same create sent twice with an `Idempotency-Key`.
  ```bash
  BODY='{"name":"Idem Demo","email":"idem.demo@example.com","title":"Analyst","department_id":3,"manager_id":3,"hire_date":"2024-05-01","salary":80000}'
  curl -si -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' -H 'Idempotency-Key: abc-123' -d "$BODY" | grep -iE "^HTTP|^location"
  curl -si -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' -H 'Idempotency-Key: abc-123' -d "$BODY" | grep -iE "^HTTP|^location|^idempotent"
  curl -s -o /dev/null -w "no key, same body: %{http_code}\n" -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' -d "$BODY"
  ```
  **Point out:** both calls return `201` with the **same** `location` (one employee); the second adds `idempotent-replayed: true`. Without a key the same body is a conflict (409, duplicate email); with a different body and the same key you get 422. Delete the employee afterwards using the id from the `location` header.
- **Ask:**
  - Q: Why is retrying a POST risky? — A: It can create duplicates.
  - Q: How does an idempotency key help? — A: The server remembers the key and returns the first result for repeats.
- **Done when:** they can explain idempotency with an example.

### Beat 3.6 — Status codes and error format
- **Slides:** 38, 39 · NEW slide: "Consistent errors, RFC 7807"
- **Say:** use 200/201/204 for success, 400 or 422 for bad input, 404 missing, 409 conflict, 500 server fault. Errors should have one shape everywhere, with enough detail to fix the request and no stack traces.
- **Demo (run: agent):** today's error shapes.
  ```bash
  curl -s http://localhost:8000/v2/employees/99999
  curl -s -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' -d '{"name":"x"}' | python3 -m json.tool
  ```
  **Point out:** 404 gives `{"detail": "..."}`; validation errors give a list with `loc`, `msg`, `type`: two shapes.
- **Demo (run: agent):** the same calls with RFC 7807 errors switched on.
  ```bash
  docker compose -f docker-compose.yml -f docker-compose.problem.yml up -d   # wait ~5s
  curl -si http://localhost:8000/v2/employees/99999 | grep -iE "^HTTP|^content-type|^\{"
  curl -s -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' -d '{"name":"x"}' | python3 -m json.tool
  curl -si -X DELETE http://localhost:8000/v2/employees | grep -iE "^HTTP|^content-type|^allow"
  docker compose up -d   # back to default errors
  ```
  **Point out:** `content-type: application/problem+json`; every error (404, 422, 405) has the same members: `type`, `title`, `status`, `detail`, `instance`; validation failures add an `errors` list with `field` and `message`.
- **Ask:**
  - Q: 400 vs 422? — A: 400 = malformed request; 422 = well-formed but invalid data (FastAPI uses 422 for validation).
  - Q: Why one error format? — A: Clients can handle every error the same way.
- **Done when:** they can map five situations to status codes.

### Beat 3.7 — List endpoints: pagination, filtering, sorting, search
- **Slides:** NEW slide(s): "Pagination styles; filter, sort, search"
- **Say:** offset/limit is simple but slow on deep pages and unstable if data changes; cursor pagination is stable. Return a total (body or `X-Total-Count`) and links. Filter with query params; sort with `?sort=-hire_date`.
- **Demo (run: agent):**
  ```bash
  B=http://localhost:8000
  curl -s "$B/v2/employees?limit=5&offset=0" | python3 -c "import sys,json; print([e['name'] for e in json.load(sys.stdin)])"
  curl -s "$B/v2/employees?limit=5&offset=5" | python3 -c "import sys,json; print([e['name'] for e in json.load(sys.stdin)])"
  curl -s "$B/v2/employees?department_id=2" | python3 -c "import sys,json; print(len(json.load(sys.stdin)), 'in Engineering')"
  curl -s -o /dev/null -w "%{http_code}\n" "$B/v2/employees?limit=1000"
  ```
  **Point out:** pages don't overlap; the filter narrows; `limit` above 100 is rejected (422).
- **Demo (run: agent):** total count, sorting and search.
  ```bash
  B=http://localhost:8000
  curl -si "$B/v2/employees?limit=2" | grep -iE "^HTTP|^x-total-count"
  curl -s "$B/v2/employees?sort=-salary&limit=3" | python3 -c "import sys,json; print([(e['name'], e['salary']) for e in json.load(sys.stdin)])"
  curl -s "$B/v2/employees?q=garcia" | python3 -c "import sys,json; print([e['name'] for e in json.load(sys.stdin)])"
  curl -s -o /dev/null -w "sort by a bad field: %{http_code}\n" "$B/v2/employees?sort=password"
  ```
  **Point out:** `x-total-count: 20` lets a client show "page 1 of 10" while only receiving 2 rows; `-salary` sorts descending (Marcus Lee first); `q` searches name, email and title; an unknown sort field is a 422 that lists the allowed ones.
- **Ask:**
  - Q: Why can offset pagination skip or repeat rows? — A: Rows inserted or deleted between pages shift the offsets.
  - Q: What do cursors fix? — A: They anchor to a position, not a count.
- **Done when:** they can page through all 20 employees.

### Beat 3.8 — Docs and tools
- **Slides:** 34, 35, 78 · NEW slide: "OpenAPI/Swagger, Postman, testing"
- **Say:** OpenAPI describes the API in machine-readable form; Swagger UI renders it; FastAPI generates it from the code. Postman for exploring, `pytest` for automated checks.
- **Demo (run: instructor):** open `http://localhost:8000/docs`, expand `POST /v2/employees`, click "Try it out", execute, read the generated `curl`.
- **Demo (run: agent):** run the starter tests, then break something on purpose.
  ```bash
  docker compose run --rm api pytest -q
  ```
  **Point out:** 8 tests pass in about a second against a throwaway SQLite database (never the Postgres data). Open `api/tests/test_api.py` and read two tests aloud: each is just "make a request, assert the status and body". Optionally change an expected value in a test, re-run, and show the failure message.
- **Ask:**
  - Q: Where does `/docs` come from? — A: Generated from the code's types and routes.
  - Q: Why automate API checks? — A: Repeatable, catches regressions.
- **Done when:** candidates have used Try it out once.

### Beat 3.9 — Advanced, one slide each (no demo unless built)
- **Slides:** NEW slide(s)
- **Say:**
  - **ETag + If-Match**: prevents lost updates (412 Precondition Failed). Demo (run: agent):
    ```bash
    B=http://localhost:8000
    ET=$(curl -si $B/v2/employees/3 | grep -i '^etag' | cut -d' ' -f2 | tr -d '\r'); echo "ETag: $ET"
    curl -s -o /dev/null -w "conditional GET: %{http_code}\n" -H "If-None-Match: $ET" $B/v2/employees/3
    curl -s -o /dev/null -w "stale If-Match:   %{http_code}\n" -X PATCH $B/v2/employees/3 -H 'Content-Type: application/json' -H 'If-Match: "stale"' -d '{"title":"Finance Director"}'
    curl -s -o /dev/null -w "current If-Match: %{http_code}\n" -X PATCH $B/v2/employees/3 -H 'Content-Type: application/json' -H "If-Match: $ET" -d '{"title":"Finance Director"}'
    ```
    **Point out:** `304` (nothing changed, save the body), `412` (someone else changed it, re-fetch), `200` (you edited the current version). Story: two HR users open the same employee; the second save is refused instead of silently overwriting the first.
  - **202 Accepted** for long-running work, with a status URL to poll.
  - **Webhooks**: the server calls you when something happens; sign and retry.
  - **Bulk and file upload**: multipart, size limits, content-type checks.
- **Ask:**
  - Q: What does a 412 tell the client? — A: Your copy is stale; fetch again before updating.
- **Done when:** the four names and their purpose are familiar.

---

## Exercise (candidates, ~30 min)
Design and call the endpoints for `leave-requests` (list, create, approve, cancel): write the table of method, path and status codes, then explain which would be idempotent. Stretch: write a `pytest` for one endpoint.

## Done-check
1. Fix three bad endpoint names.
2. Pick the method and status for each CRUD action.
3. Explain idempotency and why POST needs a key.
4. Page through a list with limit/offset and a filter.
5. Explain what OpenAPI gives you.

## Clean-up
`docker compose up -d` (problem+json off); delete the `Idem Demo` and `Legal` records or run `scripts/setup.sh --reset`.
