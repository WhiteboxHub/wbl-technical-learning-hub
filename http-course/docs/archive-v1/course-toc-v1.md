# Web, HTTP, APIs, Auth and Microservices — Table of Contents (draft v1)

Running example: **HR system** (employees, departments, managers, salary).
Environment: Docker Compose. Slide numbers refer to `updated_http.pdf` (117 slides).
Status: **Keep** = slides exist, light edit · **Fix** = slides exist, rework (students → HR, trim, reorder) · **New** = no slides yet.
Tier: **Core** = taught live · **Stretch** = brief or self-study.

---

## Part A — The Web

### 1. How the web works: HTTP foundations — Core · Keep
Request/response, client-server, URL vs URI vs URN, methods, status codes, headers, versions (1.1 / 2 / 3), persistent connections, HTTPS/TLS, HTTP caching, debugging tools.
Slides 1–19 · Demo: `curl -v` and browser Network tab against `/employees`.

### 2. Websites and the browser — Core · New
What happens when you type a URL (DNS, TCP, TLS, request, render). HTML/CSS/JS roles, the DOM. Static vs server-rendered vs SPA. How a page calls an API (`fetch`, AJAX). CDN. Same-origin policy and CORS.
Demo: a small HR directory page calling the API; trigger and fix a CORS error.

### 3. Browser storage and cookies — Core · New (+ slide 15)
Cookies vs localStorage vs sessionStorage vs IndexedDB vs Cache API. Cookie flags (HttpOnly, Secure, SameSite, Max-Age). What to store where, and why tokens are a special case.
Demo: inspect and edit storage in DevTools; watch a Set-Cookie header round trip.

### 4. JSON and data contracts — Core · Fix (moved earlier)
JSON syntax and types, JSON vs XML, JSON Schema, schema → Pydantic model → OpenAPI.
Slides 105–117 · Demo: one employee as JSON, validated against a schema.

---

## Part B — APIs

### 5. ~~Web services: SOAP vs REST~~ — removed
SOAP dropped. The short "what is a web service" intro (slides 20–24, 26) is now section 6.0 of Module 6. Module numbers are unchanged for now; renumber once the outline settles.

### 6. REST API design and CRUD — Core · Fix
API vs REST, resources and endpoints, CRUD ↔ methods, PUT vs POST, idempotency, status codes, request/response structure, Postman.
Slides 27–60 · Demo: employees and departments CRUD with nested routes. Trim slides 50–54 to ~2.

### 7. API design in practice — Core · New
Pagination, filtering, sorting. Consistent errors (RFC 7807). OpenAPI/Swagger docs. Idempotency keys, `202 Accepted` for long work, webhooks (intro).
Demo: `/employees?department=eng&page=2`, Swagger UI.

---

## Part C — Identity and Security

### 8. API authentication: basic, API key, OAuth 2.0 — Core · Fix
Authentication vs authorization, basic auth, API keys, bearer tokens, OAuth 1.0 vs 2.0, access tokens.
Slides 61–69 · Demo: the `x-auth-token` flow on the HR API.

### 9. JWT and authorization — Core · New
Sessions vs tokens, JWT anatomy (header, payload, signature), expiry and refresh, scopes, roles (RBAC).
Demo: decode a JWT; the same `GET /employees/5` returns salary to an HR admin and hides it for others.

### 10. SSO, OAuth flows and OIDC — Core · New
Authorization code + PKCE, client credentials, OIDC and ID tokens, one login across two apps, logout, MFA (intro). SAML overview (Stretch).
Demo: Keycloak login, then the same session works in the HR portal and a payroll app.

### 11. Web security essentials — Core · New
Where to store tokens in the browser, XSS, CSRF, OWASP API Top 10 highlights, input validation, TLS certificates.
Demo: a vulnerable vs fixed token store.

---

## Part D — Scaling and Architecture

### 12. API gateway: routing, rate limiting, caching, versioning — Core · Fix + New
Gateway role (routing, auth offload, CORS, logging, correlation ID). Rate limiting (fixed window, sliding window, token bucket; 429 and Retry-After). Caching (gateway vs Redis, ETag, conditional requests). Versioning (`/v1` vs `/v2`).
Slides 70–77 + new · Demo: 429 responses, cache hit/miss, v1 vs v2 behind the gateway.

### 13. Microservices — Core · Fix
Monolith vs microservices, service boundaries (DDD on HR), service discovery, load balancing, circuit breaker, timeouts and retries, health checks, sync vs async communication, CQRS and event sourcing (concepts).
Slides 81–104 · Demo: employees + departments services behind the gateway; kill one and watch the circuit breaker.

### 14. Capstone — Core · New
Trace one request from browser through gateway and services to the database with a JWT, naming every concept used. Candidate exercise: add a `leave-requests` endpoint end to end.

---

## Appendix (Stretch)
A. REST vs GraphQL vs gRPC · B. WebSockets and SSE · C. SAML · D. Saga and eventual consistency · E. Observability (logs, metrics, tracing)

---

## Each module will ship with
1. Teach script (slides to show, key points, demos in order)
2. 3–5 candidate questions with answers
3. Candidate exercise
4. Done-check for the agent
