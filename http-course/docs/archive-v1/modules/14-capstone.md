# Module 14 — Capstone (detailed TOC, draft v1)

All new. Ties every module together using one request.

## 14.1 The request we trace
`GET https://hr.local/employees/5` from the HR portal in the browser, logged in via SSO.

## 14.2 The trace, step by step
| Step | What happens | Module |
|---|---|---|
| 1 | Browser parses URL, DNS, TCP, TLS | 1, 2 |
| 2 | Page JS calls `fetch` with the access token, CORS preflight | 2, 3 |
| 3 | Gateway terminates TLS, validates JWT, applies rate limit | 9, 12 |
| 4 | Gateway checks cache, routes to employees-service | 12 |
| 5 | Service enforces role (salary field), queries Postgres | 9 |
| 6 | Service calls departments-service with timeout and circuit breaker | 13 |
| 7 | JSON response with headers (status, cache, ETag), page renders | 1, 4, 6 |

## 14.3 Concept map
- Every HTTP concept named at the point it appears: method, status, header, cookie, token, cache, CORS, version, rate limit, JSON schema

## 14.4 Live walkthrough (instructor)
- Agent runs the same request with DevTools open, `curl -v` through the gateway, gateway logs and service logs side by side, following the correlation ID

## 14.5 Break-it exercise
- Instructor injects faults one at a time; candidates diagnose from the evidence
  1. Expired token → 401
  2. Wrong role → 403
  3. Missing CORS header → browser error
  4. Rate limit hit → 429
  5. Departments-service down → 503 with fallback
  6. Cached stale data → fix invalidation

## 14.6 Candidate project
- Add a `leave-requests` feature end to end:
  - Endpoints (design, pagination, errors, OpenAPI)
  - Roles (employee creates, manager approves)
  - Gateway route and rate limit
  - SSO-protected page calling it
  - Short written trace of one request

## 14.7 Assessment rubric
- Correct HTTP semantics, status codes
- Auth and authorization
- Error handling and documentation
- Reasoning about failure
- Clarity of the trace write-up

## 14.8 Wrap-up and next steps
- Review of key takeaways per module
- Pointers: GraphQL/gRPC, observability, Kubernetes, cloud API gateways

## Candidate question bank (sample)
- Walk me through what happens when I open the HR portal.
- Where would you look first if `/employees/5` returns 502?
- Which layer should enforce authorization and why?

## Slide work
- **Add:** about 8 slides and one end-to-end diagram (new module)
