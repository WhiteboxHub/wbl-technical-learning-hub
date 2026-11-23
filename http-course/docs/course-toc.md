# Web, HTTP, APIs, Auth and Microservices — Slim Table of Contents (draft v2)

8 modules (was 13). No topic dropped: small topics are bundled onto one slide or demo ("…etc.").
Running example: **HR system** (employees, departments, managers, salary). Environment: Docker Compose.
Slide numbers refer to `updated_http.pdf`. **Have** = exists · **Fix** = rework (students → HR, trim) · **New** = no slides yet.
SOAP is out. v1 detail is kept in `archive-v1/`.

| # | Module | Folds in (v1 modules) | Existing slides | New slides (est.) |
|---|---|---|---|---|
| 1 | HTTP foundations | 1 | 1–19 | ~5 |
| 2 | Websites, browser and storage | 2, 3 | 15 | ~10 |
| 3 | JSON and REST APIs | 4, 5 (web services intro), 6, 7 | 20–60, 105–117 | ~8 |
| 4 | Authentication and tokens | 8, 9 | 61–69 | ~8 |
| 5 | SSO and web security | 10, 11 | — | ~14 |
| 6 | API gateway and scaling | 12 | 70–77 | ~6 |
| 7 | Microservices | 13 | 81–104 | ~8 |
| 8 | Capstone | 14 | — | ~5 |

About 65 new slides (was ~100).

---

## 1. HTTP foundations — Have, light edit
1. **Networking in one slide:** IP, ports, DNS, TCP vs UDP, layering. *(New)*
2. **What HTTP is:** history, text-based, stateless, client-server, proxies/gateways/CDN. (2, 3, 8)
3. **URL anatomy:** URI vs URL vs URN, scheme/host/port/path/query/fragment, encoding. (9, + New)
4. **Message anatomy:** request line, status line, headers, body, raw `nc` demo. (4, 6)
5. **Methods:** GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS etc., safe and idempotent matrix. (5, + New)
6. **Status codes:** 1xx–5xx with the ~20 you actually use, 401 vs 403 etc. (7)
7. **Headers, bodies and negotiation:** Host, Accept, Content-Type, Authorization etc.; JSON/form/multipart; redirects (301/302/307/308). (10, + New)
8. **Connections and versions:** keep-alive, HTTP/1.1, 2, 3. (11, 12)
9. **HTTPS/TLS and caching:** handshake, certificates, HSTS; Cache-Control, ETag, 304. (13, 14)
10. **Debugging:** DevTools, `curl`, Postman, mitmproxy/Wireshark. (18, 19)

Labs: raw request with `nc` then `curl -v`; every method and status against `/employees`; trigger 404/405/415/422; see a redirect and a 304.

---

## 2. Websites, browser and storage — New (+ slide 15)
1. **What happens when you type a URL:** DNS, TCP, TLS, request, render; DevTools waterfall.
2. **Anatomy of a page:** HTML/CSS/JS, DOM, sub-resources; static vs SSR vs SPA.
3. **Page calls API:** `fetch`/AJAX, JSON → DOM; web server vs app server vs reverse proxy; CDN, compression, lazy loading etc.
4. **Cookies and sessions:** Set-Cookie/Cookie, Domain/Path/Max-Age/Secure/HttpOnly/SameSite, session ID, first vs third party.
5. **Browser storage:** localStorage, sessionStorage, IndexedDB, Cache API; comparison table; what goes where.
6. **Same-origin policy and CORS:** origin, preflight `OPTIONS`, `Access-Control-*`, common mistakes.
7. *(Mention only)* WebSockets/SSE, consent banners, SEO.

Labs: record a page load; inspect cookies and storage; build the HR directory page with `fetch`; cause and fix a CORS error.

---

## 3. JSON and REST APIs — Fix + New
1. **JSON:** syntax and types, JSON vs XML, `eval` danger, JSON Schema → Pydantic → OpenAPI. (105–117)
2. **Web service, API, REST:** what a service is, REST constraints, resources, maturity model. (20–24, 26, 29–32)
3. **Endpoint design:** nouns, plurals, nesting, naming, anti-patterns. (57, + New)
4. **CRUD with methods:** GET, POST, PUT, PATCH, DELETE with request/response, `Location`, 201/204. (33–56)
5. **PUT vs POST, idempotency, retries:** trim to ~2 slides, add `Idempotency-Key`. (48–54)
6. **Status codes and error format:** 200/201/204/400/404/409/422, RFC 7807. (38, 39, + New)
7. **List endpoints:** pagination (offset vs cursor), filtering, sorting, search etc. *(New)*
8. **Docs and tools:** OpenAPI/Swagger UI, Postman collections, tests with `pytest`. (34, 35, 78)
9. **Advanced, one slide each:** `ETag`/`If-Match` concurrency, `202 Accepted`, webhooks, bulk/file upload. *(New)*

Labs: CRUD in Postman and `curl`; nested route; pagination and sorting; RFC 7807 errors; lost update fixed with ETag; first `pytest` tests.

---

## 4. Authentication and tokens — Fix + New
1. **Authentication vs authorization:** 401 vs 403. (62)
2. **Basic, API key, bearer:** how each works, weaknesses, password hashing. (61, 64, + New)
3. **OAuth 1.0 vs 2.0 concepts:** roles, access/refresh tokens, scopes. (65, 66)
4. **Sessions vs tokens.** *(New)*
5. **JWT:** header/payload/signature, claims, HS256 vs RS256, `alg:none`, never put secrets in the payload. *(New)*
6. **Token lifecycle:** expiry, refresh, rotation, revocation, validation checklist. *(New)*
7. **Authorization:** RBAC, scopes, ownership; the salary example (HR admin vs manager vs employee). *(New)*
8. **HR token flow:** `POST /token`, calling protected endpoints. (67–69 → HR)

Labs: 401 vs 403; decode and tamper with a JWT; expiry and refresh; three roles see three views of `/employees/5`.

---

## 5. SSO and web security — New
1. **Why SSO:** many apps, many passwords; IdP vs relying party.
2. **OAuth 2.0 grants:** authorization code + PKCE, client credentials, device code etc.; why implicit/password are out.
3. **Code + PKCE step by step:** redirects, `state`, code exchange.
4. **OIDC:** ID token, `openid` scope, discovery, JWKS, `/userinfo`.
5. **SSO in action, logout, MFA:** two apps one login; single logout is hard; TOTP, passkeys, step-up auth. SAML in one slide.
6. **Protecting the HR API with an IdP:** validate JWT via JWKS, map groups to roles.
7. **Token storage in the browser:** HttpOnly cookie vs localStorage vs memory.
8. **Attacks and defenses:** XSS, CSRF, SQL injection, BOLA and the OWASP API Top 10, security headers, secrets, TLS certs etc.

Labs: Keycloak realm with `hr_admin`/`manager`/`employee`; trace the login redirects; second app needs no login; exploit then fix XSS/CSRF/SQLi.

---

## 6. API gateway and scaling — Fix + New
1. **What a gateway does:** routing, TLS termination, auth offload, CORS, logging with request ID. *(New)*
2. **Rate limiting:** fixed window, sliding window, token bucket; 429, `Retry-After`; client backoff. (70, + New)
3. **Caching:** gateway vs Redis vs HTTP cache; cache-aside, TTL, invalidation. (72–76)
4. **Versioning and deprecation:** URL/header, `Sunset`. (71)
5. **Gateway and security:** auth at the edge, trust boundary, size limits etc.

Labs: route through the gateway; trigger 429; cache hit/miss and invalidation; `/v1` and `/v2` side by side.

---

## 7. Microservices — Fix + New
1. **Monolith and its limits; what microservices are; when not to use them.** (82–90)
2. **Splitting the HR monolith:** bounded contexts, database per service. *(New)*
3. **DDD in brief.** (95, 96)
4. **Communication:** REST, gRPC, queues and events; sync vs async. (101–104)
5. **Discovery, load balancing, resilience:** timeouts, retries, circuit breaker, bulkhead. (91, + New)
6. **CQRS and event sourcing (concepts).** (97–100)
7. **Operating them:** containers, health checks, correlation ID, tracing; saga and eventual consistency in one slide.
8. **Testing and deployment:** contract tests, CI/CD per service. (one slide)

Labs: gateway + employees + departments + postgres; cross-service call; kill a service and add a circuit breaker; `EmployeeHired` event.

---

## 8. Capstone — New
1. Trace `GET /employees/5` through browser → gateway → service → database with a JWT, naming each concept.
2. Break-it exercise: expired token, wrong role, CORS, 429, service down, stale cache.
3. Candidate project: add `leave-requests` end to end.
4. Rubric and wrap-up; pointers (GraphQL/gRPC, observability, Kubernetes).

---

## Every module ships with
Teach script · 3–5 candidate questions with answers · exercise · done-check.

## Open points
- Module 3 is the largest. If class time is short, split it at "list endpoints" into 3a and 3b.
- Image-only slides (31, 58, 63, 77, 87, 88, 92, 98, 100, 103) need review. Slide 107 has a "SOAP" copy error.
- Module 0 (tooling prerequisites) is handled by the setup skill, not by a module.
