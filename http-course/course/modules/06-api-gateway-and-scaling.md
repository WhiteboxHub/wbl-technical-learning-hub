# Module 6 — API Gateway and Scaling

Teach-skill content file. All demos run on the current stack (verified live through the gateway).
Time: about 75 minutes.

## Objectives
Explain what an API gateway does; demonstrate rate limiting (429, `Retry-After`) and caching (hit/miss, invalidation); run two API versions side by side and deprecate one; explain where security belongs at the edge.

## Stack requirements
`scripts/setup.sh` READY: nginx gateway on `http://localhost:8080` (config in `gateway/nginx.conf`), Redis on `:6379`, API on `:8000`. The gateway adds `X-Request-Id`, rate-limits `GET /v2/limited` (5 per minute per client; 429 + `Retry-After`), routes `/v1/*` to the API with `Deprecation` and `Sunset` headers, and requires an `Authorization` header on `/secure/*`. The API caches `GET /v2/departments` in Redis for 30 s (cache-aside) and reports `X-Cache-Status: HIT|MISS`. **The rate limiter counts per minute: if you re-run Beat 6.2 within a minute you will get 429s immediately; run `docker compose restart gateway` to reset it.**

---

### Beat 6.1 — What a gateway does
- **Slides:** NEW slides: "API gateway: single entry point", "Gateway vs reverse proxy vs load balancer"
- **Say:** one front door for all APIs: routing and path rewriting, TLS termination, authentication at the edge, CORS, rate limiting, caching, logging with a request ID, circuit breaking. Tools: nginx, Traefik, Kong, cloud gateways. Services behind it can stay simple.
- **Demo (run: agent):** the same API through the gateway.
  ```bash
  curl -si http://localhost:8080/v2/employees/1 | grep -iE "^HTTP|^content-type|^x-request-id"
  curl -si http://localhost:8000/v2/employees/1 | grep -iE "^HTTP|^content-type|^x-request-id"
  ```
  **Point out:** same JSON through both ports, but only the gateway adds `x-request-id`. Clients should know only the gateway's port (8080).
- **Ask:**
  - Q: Name three jobs a gateway can take off each service. — A: TLS, auth, rate limiting, logging, CORS, caching.
  - Q: What is a request ID for? — A: Following one request through logs across services.
- **Done when:** they can draw client → gateway → services.

### Beat 6.2 — Rate limiting
- **Slides:** 70 · NEW slide: "Algorithms: fixed window, sliding window, token bucket; 429 and Retry-After"
- **Say:**
  - Why: abuse, fairness, cost, protection. Key limits by IP, user or API key.
  - **Fixed window**: simple, but allows a burst at the boundary. **Sliding window**: smoother. **Token bucket**: allows controlled bursts and a steady rate.
  - Response: `429 Too Many Requests` plus `Retry-After`; clients back off with jitter.
- **Demo (run: agent):** trip the limit.
  ```bash
  for i in $(seq 1 8); do curl -s -o /dev/null -w "request $i: %{http_code}\n" http://localhost:8080/v2/limited; done
  curl -si http://localhost:8080/v2/limited | grep -iE "^HTTP|retry-after"
  ```
  **Point out:** 200 for the first five, then 429; `retry-after: 12` tells the client when to try again. (Counts per minute; restart the gateway to reset it.)
- **Ask:**
  - Q: What should a client do on 429? — A: Wait for `Retry-After`, then retry with backoff and jitter.
  - Q: Token bucket vs fixed window? — A: Token bucket allows bursts at a steady average; fixed windows can double up at the boundary.
- **Done when:** they can describe one algorithm.

### Beat 6.3 — Caching
- **Slides:** 72–76 · NEW slide: "Gateway cache vs Redis; cache-aside, TTL, invalidation"
- **Say:** cache at several layers: browser, gateway, application (Redis), database. Cache-aside: look in cache, on miss read the database and store it. TTL bounds staleness. Invalidation is the hard part. In HR: cache the departments list; do not cache salary views or per-user data. Use `Cache-Control` and `ETag` (Module 1 Beat 1.9).
- **Demo (run: agent):** miss, hit, invalidate.
  ```bash
  G=http://localhost:8080
  docker compose exec -T redis redis-cli DEL departments:list > /dev/null     # start cold
  curl -si $G/v2/departments | grep -i x-cache-status
  curl -si $G/v2/departments | grep -i x-cache-status
  ID=$(curl -si -X POST $G/v2/departments -H 'Content-Type: application/json' -d '{"name":"Legal","location":"Austin"}' | grep -i '^location' | sed 's#.*/##' | tr -d '\r')
  curl -si $G/v2/departments | grep -i x-cache-status
  curl -s -o /dev/null -w "cleanup: %{http_code}\n" -X DELETE $G/v2/departments/$ID
  docker compose exec -T redis redis-cli TTL departments:list
  ```
  **Point out:** MISS (read the database, stored in Redis), HIT (served from Redis), MISS again after the write invalidated the key, then a fresh entry whose TTL counts down from 30. This is cache-aside implemented in the application with Redis; the gateway itself is a pass-through here.
- **Ask:**
  - Q: Why not cache `/employees/5` with salary for everyone? — A: Different users may see different data; a shared cache could leak it.
  - Q: What does a TTL trade off? — A: Freshness against load.
- **Done when:** they can explain hit, miss and invalidation.

### Beat 6.4 — Versioning and deprecation
- **Slides:** 71 · NEW slide: "Breaking vs non-breaking changes; Deprecation and Sunset"
- **Say:** breaking changes (removing a field, changing meaning) need a new version: URL (`/v1`, `/v2`), header, or media type. Non-breaking changes (adding optional fields) don't. Announce retirement with `Deprecation` and `Sunset` headers and a migration path.
- **Demo (run: agent):**
  ```bash
  curl -si http://localhost:8080/v1/employees/1 | grep -iE "^HTTP|deprecation|sunset"
  curl -si http://localhost:8080/v2/employees/1 | grep -iE "^HTTP|deprecation|sunset"
  ```
  **Point out:** v1 answers but warns; v2 is clean.
- **Ask:**
  - Q: Is adding a new optional field a breaking change? — A: No. Removing or renaming one is.
- **Done when:** they can classify three changes.

### Beat 6.5 — Gateway and security
- **Slides:** NEW slide
- **Say:** validate tokens at the edge, but still check authorization in the service; set request size limits; allow-list IPs for admin routes; the gateway is a trust boundary, so services should not be reachable around it.
- **Demo (run: agent):**
  ```bash
  curl -si http://localhost:8080/secure/employees/1 | grep -iE "^HTTP|^\{"
  curl -s -o /dev/null -w "with an Authorization header: %{http_code}\n" -H "Authorization: Bearer anything" http://localhost:8080/secure/employees/1
  ```
  **Point out:** with no header the gateway itself answers `401` and the API never sees the request. With any header it passes the request through (this demo gateway only checks presence; the API validates the token for real when auth is on, which is the point of defense in depth).
- **Ask:**
  - Q: If the gateway checks the token, can the service skip authorization? — A: No; defense in depth, and services can be reached internally.
- **Done when:** they can name two edge protections.

---

## Exercise (candidates, ~25 min)
Add a stricter limit (2 requests/minute) to `GET /v2/employees/{id}/salary` through the gateway config, prove it with a loop of requests, and explain which key you limited by and why.

## Done-check
1. Name five gateway responsibilities.
2. Explain 429 and `Retry-After`.
3. Describe a cache hit, miss and invalidation.
4. Classify breaking and non-breaking changes.
5. Explain why authorization still belongs in the service.

## Clean-up
Delete demo records; `scripts/setup.sh --reset`.
