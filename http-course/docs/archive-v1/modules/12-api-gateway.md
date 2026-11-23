# Module 12 — API Gateway: Routing, Rate Limiting, Caching, Versioning (detailed TOC, draft v1)

Status: **Have** (slides 70–76 on rate limiting, versioning, caching) · **Thin** · **Add**

## 12.1 What is an API gateway
- Single entry point in front of services; reverse proxy plus policies
- Gateway vs reverse proxy vs load balancer vs service mesh
- Tools: nginx, Traefik, Kong, AWS API Gateway
**Add** (slide 91 mentions it in one line)

## 12.2 Gateway responsibilities
- Routing and path rewriting, TLS termination, auth offload (validate JWT)
- CORS handling, request/response transformation
- Logging, metrics, correlation/request ID
- Rate limiting, caching, circuit breaking
**Add**

## 12.3 Rate limiting
- Why: abuse, fairness, cost, protection
- Algorithms: fixed window, sliding window, token bucket, leaky bucket
- Keys: per IP, per user, per API key, per route
- Responses: `429 Too Many Requests`, `Retry-After`, `X-RateLimit-*`
- Client behavior: backoff and jitter
Slide 70 · **Thin** (algorithms and headers to add)

## 12.4 Caching
- Why cache; client vs gateway vs application (Redis) vs database
- Cache-aside, TTL, invalidation, stale data
- HTTP caching in the API: `Cache-Control`, `ETag`, `304`
- What to cache in HR (departments list) and what not (salary views)
Slides 72–76 · **Have** (add Redis and gateway cache)

## 12.5 API versioning
- Why versions break clients
- URL (`/v1`, `/v2`), header, query param, media type
- Deprecation: `Deprecation` and `Sunset` headers
- Backward-compatible vs breaking changes
Slide 71 · **Have** (add deprecation)

## 12.6 Gateway and security
- Authentication at the edge, IP allow-lists, request size limits
- Trust boundary: services behind the gateway

## 12.7 Observability at the edge
- Access logs, request IDs propagated downstream, basic metrics

## 12.8 Demo architecture
```
client → gateway (nginx/Traefik) → employees-service → postgres
                                 → departments-service
                         redis (cache, rate-limit counters)
```

## Labs
1. Route `/employees` and `/departments` through the gateway
2. Set 5 requests/minute and watch the 429 and `Retry-After`
3. Cache `GET /departments`, show hit vs miss and invalidation on POST
4. Run `/v1` and `/v2` side by side, deprecate `/v1`
5. Candidate exercise: add a stricter limit for `/employees/{id}/salary`

## Candidate question bank (sample)
- Fixed window vs token bucket?
- What should the client do on 429?
- What is cache invalidation and why is it hard?

## Slide work
- **Fix:** 70–76 to HR and gateway framing
- **Add:** gateway intro, responsibilities, algorithm diagrams (about 8 slides)
