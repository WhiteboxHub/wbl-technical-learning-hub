# Module 6 — REST API Design and CRUD (detailed TOC, draft v1)

Status: **Have** · **Thin** · **Add**. Students → HR throughout (slides 36–57 use `/v2/students`).

## 6.0 What is a web service (moved from the old Module 5; SOAP dropped)
- Machine-to-machine communication over a network
- Messenger analogy: request → process → response
- Web service vs website vs API
- REST is the style this course uses
- Everyday examples: maps, weather, payments, login with Google; HR: payroll lookup, benefits provider
Slides 20–26, 79 · **Have** (swap weather example for HR; drop the SOAP example slide 25 and the REST-vs-SOAP slide 79)

## 6.1 What is an API
- Definition, contract between systems, library API vs web API
Slide 29 · **Have**

## 6.2 What is REST
- Representational State Transfer, Roy Fielding, architectural style not a protocol
- Resources and representations
Slide 30 · **Have**

## 6.3 REST constraints
- Client-server, stateless, cacheable, uniform interface, layered system, code on demand (optional)
- What "RESTful" means vs "HTTP API"
- Richardson maturity model (levels 0–3, HATEOAS awareness)
Slide 32 · **Thin** (maturity model to add)

## 6.4 Resources and endpoint design
- Nouns not verbs, plural collections, nesting, IDs
- `GET /employees`, `GET /employees/{id}`, `GET /departments/{id}/employees`
- Naming conventions, trailing slash, lowercase, hyphens
- Anti-patterns: `/getEmployee`, `/employees/delete/5`
Slide 57 · **Have** (rewrite for HR, add anti-patterns)

## 6.5 HTTP methods as CRUD
- Create → POST, Read → GET, Update → PUT/PATCH, Delete → DELETE
Slide 33 · **Have**

## 6.6 GET — read
- List and single; query params; 200 and 404; JSON response
Slides 36, 37, 40 · **Have** (HR)

## 6.7 POST — create
- Request headers and body, `Content-Type`, 201 Created, `Location` header, 400/422 validation
Slides 41–44 · **Have**

## 6.8 PUT — replace/update
- Full replacement, idempotent, 200/204, 404
Slides 45–47 · **Have**

## 6.9 PATCH — partial update
- PUT vs PATCH, JSON Merge Patch vs JSON Patch (awareness)
**Add**

## 6.10 DELETE
- 204 vs 200 with message, idempotency, soft delete vs hard delete
Slides 55, 56 · **Have**

## 6.11 PUT vs POST, idempotency
- Idempotent vs not, with a double-click/retry story
- When each is used for create/update
Slides 48–54 · **Thin to trim**: cut interchangeability slides 50–54 to about 2

## 6.12 Request and response structure
- Request: method, URL, headers (Content-Type, Accept, Authorization), body
- Response: status code, headers, body
Slides 41, 59, 60 · **Have**

## 6.13 Status codes in REST
- 200, 201, 204, 400, 401, 403, 404, 405, 409, 422, 500 and when to use each
Slides 38, 39 · **Have** (add 409, 422 mapping)

## 6.14 Postman
- Install, collections, environments, variables, tests
- Running the HR collection
Slides 34, 35, 40, 44, 47, 56 · **Have**

## 6.15 Tools and use cases
- curl, httpie, Insomnia, Swagger UI
- Real-world APIs: social, payments, maps
Slides 78, 80 · **Have**

## Labs
1. Full CRUD on `/employees` in Postman, then in `curl`
2. Nested route: employees of a department
3. Break each rule on purpose and read the status code
4. Retry a POST vs a PUT and compare the result
5. Candidate exercise: design the endpoints for `leave-requests`

## Candidate question bank (sample)
- Why plural nouns?
- PUT vs PATCH vs POST?
- Which status code for a created resource? For a validation error?
- Is `DELETE /employees/5` idempotent?

## Slide work
- **Fix:** students → employees (slides 36–57); trim 50–54
- **Add:** REST maturity model, PATCH, anti-patterns (about 4 slides)
