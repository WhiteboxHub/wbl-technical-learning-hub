# Module 1 — How the Web Works: HTTP Foundations (detailed TOC, draft v1)

Slide refs = `updated_http.pdf`. Status: **Have** = covered by a slide · **Thin** = slide exists but shallow · **Add** = missing, needs a new slide.
Demo target: HR API (`/employees`, `/departments`) via Docker Compose.

## 1.1 Networking prelude
- Internet, IP address, port, hostname
- DNS in one slide (name → IP)
- TCP vs UDP; HTTP rides on TCP (HTTP/3 on QUIC/UDP)
- Layering: HTTP → TLS → TCP → IP
- Well-known ports: 80, 443, 8000
Status: **Add** (slide 8 touches TCP only)

## 1.2 What is HTTP
- Definition, purpose, history (0.9 → 1.0 → 1.1 → 2 → 3)
- Text-based, request/response, **stateless**
Slides 2, 8 · **Have**

## 1.3 Client-server architecture
- Client (browser, app, curl), server
- Intermediaries: forward proxy, reverse proxy, load balancer, gateway, CDN
Slide 3 · **Thin** (intermediaries need a diagram)

## 1.4 URLs: URI vs URL vs URN
- URI (identifier) vs URL (locator) vs URN (name), with examples
- URL anatomy: scheme, userinfo, host, port, path, query string, fragment
- Path params vs query params (`/employees/5` vs `/employees?dept=eng`)
- Percent-encoding (`%20`), reserved characters
- Absolute vs relative URLs
Slide 9 · **Thin** (anatomy, encoding, params to add)

## 1.5 Anatomy of an HTTP message
- Request: request line (method, target, version), headers, blank line, body
- Response: status line (version, code, reason), headers, blank line, body
- Raw message on the wire (`nc`/`telnet` demo)
Slides 4, 6 · **Have**

## 1.6 HTTP methods
- GET, POST, PUT, PATCH, DELETE
- HEAD, OPTIONS (and preflight preview), TRACE, CONNECT (awareness)
- **Safe** and **idempotent** matrix, cacheable or not, body or not
- Method vs intent: why GET must not change state
Slide 5 · **Thin** (PATCH, HEAD, OPTIONS, safe/idempotent matrix to add)

## 1.7 Status codes
- 1xx: 100 Continue, 101 Switching Protocols
- 2xx: 200, 201, 202, 204
- 3xx: 301, 302, 304, 307, 308
- 4xx: 400, 401, 403, 404, 405, 409, 415, 422, 429
- 5xx: 500, 502, 503, 504
- 401 vs 403, 404 vs 410, 502 vs 504
Slide 7 · **Thin** (list exists, no "which to use when")

## 1.8 Headers
- Categories: general, request, response, representation (entity)
- Request: Host, User-Agent, Accept, Accept-Language, Accept-Encoding, Authorization, Cookie, Origin, Referer
- Response: Server, Location, Set-Cookie, Content-Length, Retry-After
- Representation: Content-Type, Content-Encoding, Content-Length
- Custom headers (`X-` convention, why it's discouraged now)
- **Content negotiation** (Accept → Content-Type)
Slide 10 · **Thin** (negotiation to add)

## 1.9 Request and response bodies
- JSON, form-urlencoded, multipart/form-data, plain text, HTML, binary
- Charset, compression (gzip/br)
- Which methods carry a body
**Add**

## 1.10 Redirects
- 301 vs 302 vs 307 vs 308, `Location` header
- Redirect chains and loops, method preservation
**Add**

## 1.11 Connections and HTTP versions
- Non-persistent vs persistent (keep-alive)
- HTTP/1.1: pipelining, head-of-line blocking
- HTTP/2: multiplexing, header compression, server push
- HTTP/3: QUIC
- Comparison table
Slides 11, 12 · **Have**

## 1.12 HTTPS and TLS
- Why: confidentiality, integrity, authentication
- TLS handshake overview, certificates, CAs, chain of trust
- HSTS, mixed content
- Demo: inspect a certificate in the browser
Slide 13 · **Thin** (handshake and certificates to add)

## 1.13 HTTP caching
- `Cache-Control` (max-age, no-store, no-cache, public, private)
- Validators: `ETag` + `If-None-Match`, `Last-Modified` + `If-Modified-Since`, 304 Not Modified
- Browser cache vs shared cache (proxy/CDN)
Slide 14 · **Thin** (validators and 304 flow to add)

## 1.14 Statelessness and cookies (intro)
- Stateless protocol → how state is faked: cookies and sessions
- `Set-Cookie` / `Cookie` round trip
- Full treatment in Module 3
Slide 15 · **Have** (as intro)

## 1.15 Authentication in HTTP (intro)
- Basic auth (Base64 is not encryption), Bearer token
- `Authorization` header, `WWW-Authenticate`, 401 vs 403
- Full treatment in Modules 8–10
Slide 16 · **Have** (as intro)

## 1.16 HTTP and REST (preview)
- REST uses HTTP methods, status codes, URLs
- Full treatment in Module 6
Slide 17 · **Have**

## 1.17 Debugging HTTP
- Browser DevTools Network tab (timing, headers, payload)
- `curl`: `-v`, `-i`, `-X`, `-H`, `-d`, `-L`, `-o`
- Postman, httpie
- Proxies and sniffers: Fiddler, mitmproxy, Wireshark
Slides 18, 19 · **Have** (swap Fiddler link for mitmproxy)

## 1.18 Labs (HR API)
1. Raw request with `nc`, then the same with `curl -v`
2. Each method against `/employees` and read the status codes
3. Trigger 404, 405, 415, 422 on purpose
4. Observe a redirect and a 304
5. Inspect headers and caching in DevTools
6. Candidate exercise: write 5 curl commands to fetch, create, update, delete and list employees

## Candidate question bank (sample)
- Difference between URI, URL and URN?
- Why is GET "safe" but PUT only "idempotent"?
- 401 vs 403?
- What does a 304 save?
- Why can't HTTP remember who you are?
- What problem does HTTP/2 multiplexing solve?

## Slide work for this module
- **Add (new slides):** networking prelude, URL anatomy and encoding, bodies and content types, redirects, content negotiation
- **Thin (extend):** intermediaries diagram, methods matrix, status-code usage guide, TLS handshake, caching validators
- **Have:** 2, 4, 6, 11, 12, 14–17, 18, 19 with light edits
