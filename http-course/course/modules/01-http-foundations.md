# Module 1 — HTTP Foundations

Teach-skill content file. Format is described in `.claude/skills/teach-http-class/SKILL.md`.
Deck: `updated_http.pdf` (slide numbers below). **NEW slide** = not in the deck yet; teach from the "Say" points and the demo.
Stack: HR API at `http://localhost:8000` (`scripts/setup.sh` must be READY).
Time: about 75–90 minutes with demos and questions.

## Objectives
By the end, candidates can read and write a raw HTTP request/response, choose methods and status codes, explain URL parts and key headers, and use `curl` and DevTools to inspect traffic.

---

### Beat 1.1 — How a request travels (networking in one slide)
- **Slides:** 8 · NEW slide: "IP, port, DNS, TCP: what sits under HTTP"
- **Say:**
  - A hostname becomes an IP address (DNS); a port picks the program on that machine.
  - HTTP is a text conversation that rides on a TCP connection (HTTP/3 uses QUIC). Layers: HTTP → TLS → TCP → IP.
  - Well-known ports: 80 HTTP, 443 HTTPS; our API is on 8000.
- **Demo (run: agent):**
  ```bash
  curl -sv http://localhost:8000/health -o /dev/null 2>&1 | grep -E "Trying|Connected|> GET|< HTTP"
  ```
  **Point out:** "Trying … :8000" is the TCP connect to an IP and port; `> GET` is the request we send; `< HTTP/1.1 200 OK` is the reply.
- **Ask:**
  - Q: What does DNS do? — A: Turns a hostname into an IP address.
  - Q: Why do we need a port as well as an IP address? — A: The IP finds the machine; the port finds the program on it.
- **Done when:** candidates can say "hostname → IP, port → program, HTTP over TCP".

### Beat 1.2 — What HTTP is
- **Slides:** 2, 3, 8
- **Say:**
  - A protocol for client–server requests and responses; text-based; **stateless**: the server does not remember the last request.
  - Clients: browsers, apps, `curl`. Servers: our FastAPI app. In between can sit proxies, load balancers, gateways, CDNs.
  - History in one line: 0.9 → 1.0 → 1.1 → 2 → 3.
- **Demo (run: agent):** same request twice, nothing carries over.
  ```bash
  curl -s http://localhost:8000/v2/employees/1; echo; curl -s http://localhost:8000/v2/employees/1; echo
  ```
  **Point out:** identical answers; the second call carries no memory of the first. Cookies and tokens (later) are how state is faked.
- **Ask:**
  - Q: What does "stateless" mean? — A: Each request must contain everything the server needs; the server keeps no memory between requests.
  - Q: Name two things that can sit between client and server. — A: Proxy, load balancer, gateway, CDN, cache.
- **Done when:** "stateless" is explained in their own words.

### Beat 1.3 — URLs: URI vs URL vs URN
- **Slides:** 9 · NEW slide: "Anatomy of a URL + percent-encoding"
- **Say:**
  - URI identifies a resource; URL says where it is and how to get it; URN names it regardless of location (e.g. `urn:isbn:…`). Every URL is a URI.
  - Anatomy: `http://localhost:8000/v2/employees?department_id=2&limit=3#top`: scheme, host, port, path, query, fragment (the fragment never goes to the server).
  - Path identifies the resource (`/employees/5`); query refines it (`?department_id=2`).
  - Special characters are percent-encoded (`space` → `%20`).
- **Demo (run: agent):**
  ```bash
  curl -s "http://localhost:8000/v2/employees?department_id=2&limit=3" | python3 -m json.tool | head -20
  python3 -c "import urllib.parse; print(urllib.parse.quote('Engineering & Ops'))"
  ```
  **Point out:** the query string filtered to Engineering and limited to 3; the second command prints `Engineering%20%26%20Ops`.
- **Ask:**
  - Q: Is every URI a URL? — A: No; a URN is a URI that is not a locator. Every URL is a URI.
  - Q: Which part of a URL does the server never see? — A: The fragment (`#…`).
  - Q: Path param or query param for "employees in department 2"? — A: Either `/departments/2/employees` or `?department_id=2`; path for identity, query for filtering.
- **Done when:** they can label each part of a URL.

### Beat 1.4 — Anatomy of an HTTP message
- **Slides:** 4, 6
- **Say:**
  - Request: request line (method, target, version), headers, blank line, optional body.
  - Response: status line (version, code, reason), headers, blank line, body.
  - It is plain text; `curl` and browsers just format it.
- **Demo (run: agent):** hand-written request over a raw socket.
  ```bash
  (printf 'GET /v2/employees/1 HTTP/1.1\r\nHost: localhost\r\nConnection: close\r\n\r\n'; sleep 1) | nc -w 2 localhost 8000
  ```
  **Point out:** we typed exactly four lines; the blank line ends the headers; the reply has a status line, headers, blank line, JSON body.
- **Ask:**
  - Q: What separates headers from body? — A: An empty line.
  - Q: Which three things are on the request line? — A: Method, target (path+query), HTTP version.
- **Done when:** they can point at each part in the raw output.

### Beat 1.5 — Methods
- **Slides:** 5 · NEW slide: "Methods, safe vs idempotent matrix (+ PATCH, HEAD, OPTIONS)"
- **Say:**
  - GET read, POST create, PUT replace, PATCH partial update, DELETE remove; HEAD = GET without body; OPTIONS = what is allowed.
  - **Safe** = does not change state (GET, HEAD, OPTIONS). **Idempotent** = repeating gives the same end state (GET, PUT, DELETE, not POST).
  - GET must never change data.
- **Demo (run: agent):** full lifecycle on one employee. Use a unique email; capture `ID` from the `Location` header of the POST.
  ```bash
  EMAIL=class.demo.$(date +%s)@example.com
  curl -si -X POST http://localhost:8000/v2/employees -H 'Content-Type: application/json' \
    -d "{\"name\":\"Class Demo\",\"email\":\"$EMAIL\",\"title\":\"Analyst\",\"department_id\":3,\"manager_id\":3,\"hire_date\":\"2024-05-01\",\"salary\":80000}"
  curl -s http://localhost:8000/v2/employees/$ID
  curl -si -X PUT http://localhost:8000/v2/employees/$ID -H 'Content-Type: application/json' \
    -d "{\"name\":\"Class Demo\",\"email\":\"$EMAIL\",\"title\":\"Senior Analyst\",\"department_id\":3,\"manager_id\":3,\"hire_date\":\"2024-05-01\",\"salary\":90000}"
  curl -si -X PATCH http://localhost:8000/v2/employees/$ID -H 'Content-Type: application/json' -d '{"salary":95000}'
  curl -si -X DELETE http://localhost:8000/v2/employees/$ID
  ```
  **Point out:** POST → `201 Created` plus a `location` header; PUT sends the whole object; PATCH sends only the changed field; DELETE → `204` with no body. Run DELETE twice to show the second is 404 (idempotent end state, different response).
  Then HEAD on a public server, and a wrong method on ours:
  ```bash
  curl -sI https://example.com | head -3
  curl -si -X DELETE http://localhost:8000/v2/employees | grep -iE "^HTTP|^allow"
  ```
  **Point out:** HEAD returns headers only, no body. Our collection route answers `405 Method Not Allowed` with an `allow: GET` header listing what it does accept. That is also what `OPTIONS` is for in general; our API does not implement `HEAD` or `OPTIONS`, and `OPTIONS` matters again for CORS in Module 2.
- **Ask:**
  - Q: PUT vs PATCH? — A: PUT replaces the whole resource; PATCH changes only the fields sent.
  - Q: Why is POST not idempotent? — A: Repeating it creates another resource each time.
  - Q: Why must GET never change data? — A: Browsers, caches, crawlers and prefetchers assume GET is safe and repeat it freely.
- **Done when:** they can say which method for create / read / replace / update / delete and which are safe or idempotent.

### Beat 1.6 — Status codes
- **Slides:** 7
- **Say:**
  - 1xx info, 2xx success, 3xx redirect, 4xx client's fault, 5xx server's fault.
  - Codes you will use: 200, 201, 204, 301/302/307/308, 304, 400, 401, 403, 404, 405, 409, 422, 429, 500, 502, 503, 504.
  - 401 = "who are you?" (not authenticated); 403 = "I know you, but no" (not allowed). 502/504 = a gateway or proxy got a bad answer or timed out.
- **Demo (run: agent):** provoke each on purpose.
  ```bash
  B=http://localhost:8000
  curl -s -o /dev/null -w "%{http_code}  OK read\n"            $B/v2/employees/1
  curl -s -o /dev/null -w "%{http_code}  not found\n"          $B/v2/employees/99999
  curl -s -o /dev/null -w "%{http_code}  method not allowed\n" -X DELETE $B/v2/employees
  curl -s -o /dev/null -w "%{http_code}  validation error\n"   -X POST $B/v2/employees -H 'Content-Type: application/json' -d '{"name":"x"}'
  curl -s -o /dev/null -w "%{http_code}  conflict\n"           -X DELETE $B/v2/departments/2
  curl -s -o /dev/null -w "%{http_code}  redirect\n"           $B/v2/employees/
  ```
  **Point out:** 200, 404, 405, 422, 409 (department still has employees), 307. 401/403 appear in Module 4 when auth exists.
- **Ask:**
  - Q: 401 or 403: logged in as a normal user, deleting someone else's record? — A: 403.
  - Q: Which code for "created"? For "deleted, nothing to return"? — A: 201; 204.
  - Q: Who is at fault for a 4xx? A 5xx? — A: The client; the server.
  - Q: What does a 502 tell you? — A: A gateway/proxy got a bad response from the server behind it.
- **Done when:** they can pick the right code for five described situations.

### Beat 1.7 — Headers, bodies, content negotiation, redirects
- **Slides:** 10 · NEW slide: "Content types, negotiation, redirects"
- **Say:**
  - Headers are key–value metadata. Request: `Host`, `User-Agent`, `Accept`, `Authorization`, `Cookie`. Response: `Server`, `Location`, `Set-Cookie`, `Content-Length`. Representation: `Content-Type`, `Content-Encoding`.
  - `Accept` (what I want) vs `Content-Type` (what this body is). Bodies: JSON, form-urlencoded, multipart, HTML, binary.
  - Redirects: 301/308 permanent, 302/307 temporary; 307/308 keep the method. `Location` says where to go.
- **Demo (run: agent):**
  ```bash
  curl -si http://localhost:8000/v2/employees/1 | head -8
  curl -si -H "Accept: text/html" http://localhost:8000/v2/employees/1 | head -1
  curl -si -X POST http://localhost:8000/v2/departments -H 'Content-Type: text/plain' -d 'hello' | head -1
  curl -siL http://localhost:8000/v2/employees/ | grep -E "^HTTP|^location"
  ```
  **Point out:** response headers (`content-type: application/json`, `content-length`); our API ignores `Accept` and always answers JSON (a server that honors negotiation could return 406 or HTML); the wrong `Content-Type` is rejected with 422 here (some servers use 415); `-L` follows the 307 from `/v2/employees/` to `/v2/employees`.
- **Ask:**
  - Q: `Accept` vs `Content-Type`? — A: Accept = formats the client can take; Content-Type = format of the body being sent.
  - Q: 301 vs 307? — A: Permanent vs temporary; 307 keeps the method and body.
- **Done when:** they can name five headers and say which direction each goes.

### Beat 1.8 — Connections and HTTP versions
- **Slides:** 11, 12
- **Say:**
  - Non-persistent: new TCP connection per request. Persistent (keep-alive, default in 1.1): reuse the connection.
  - HTTP/1.1: head-of-line blocking. HTTP/2: multiplexing many requests on one connection, header compression. HTTP/3: QUIC over UDP, faster setup.
- **Demo (run: agent):**
  ```bash
  curl -sv http://localhost:8000/health http://localhost:8000/health -o /dev/null -o /dev/null 2>&1 | grep -iE "Connected to|Re-using"
  curl -sI --http1.1 https://example.com | head -1
  curl -sI --http2 https://example.com | head -1
  ```
  **Point out:** "Re-using existing connection" is keep-alive; the same site answers as `HTTP/1.1` and `HTTP/2`.
- **Ask:**
  - Q: What does keep-alive save? — A: The cost of a new TCP (and TLS) handshake per request.
  - Q: What problem does HTTP/2 multiplexing solve? — A: Requests no longer queue behind each other on one connection.
- **Done when:** they can explain keep-alive and one benefit of HTTP/2.

### Beat 1.9 — HTTPS/TLS and caching
- **Slides:** 13, 14 · NEW slide: "TLS handshake and validators (ETag, 304)"
- **Say:**
  - HTTPS = HTTP inside TLS: encryption, integrity, server identity. A certificate signed by a trusted CA proves the host; the handshake agrees on keys. HSTS tells browsers to always use HTTPS.
  - Caching: `Cache-Control` (max-age, no-store, no-cache, public, private). Validators: `ETag`/`If-None-Match`, `Last-Modified`/`If-Modified-Since` → `304 Not Modified` saves the body.
- **Demo (run: agent, needs internet):**
  ```bash
  curl -svI https://example.com 2>&1 | grep -E "TLSv|subject:|issuer:|expire date"
  LM=$(curl -sI https://example.com | grep -i '^last-modified' | cut -d' ' -f2- | tr -d '\r')
  curl -sI -H "If-Modified-Since: $LM" https://example.com | head -1
  ```
  **Point out:** TLS version, certificate subject, issuer and expiry; the conditional request returns `304` with no body. If offline, explain with the slides only and say so.
- **Ask:**
  - Q: What three things does TLS give you? — A: Confidentiality, integrity, authentication of the server.
  - Q: What does a 304 mean and what does it save? — A: "Your cached copy is still good"; the body transfer.
  - Q: `no-cache` vs `no-store`? — A: no-cache = may store but must revalidate; no-store = never store.
- **Done when:** they can describe the 304 round trip.

### Beat 1.10 — Cookies, auth and REST previews (no demo)
- **Slides:** 15, 16, 17
- **Say:** Stateless HTTP fakes state with cookies (`Set-Cookie` / `Cookie`) — Module 2. Auth rides in the `Authorization` header (Basic, Bearer) — Module 4. REST is a style built on exactly these methods, URLs and status codes — Module 3.
- **Ask:**
  - Q: How can a stateless protocol "remember" a logged-in user? — A: The client sends something with every request: a cookie or token.
- **Done when:** they know where each topic is coming.

### Beat 1.11 — Debugging HTTP
- **Slides:** 18, 19
- **Say:** Browser DevTools Network tab, `curl` (`-v` `-i` `-X` `-H` `-d` `-L` `-o`), Postman, and proxies/sniffers (mitmproxy, Wireshark; Fiddler is dated).
- **Demo (run: instructor):** open `http://localhost:8000/docs` in the browser, open DevTools → Network, click "Try it out" on `GET /v2/employees`, then show request headers, response headers, status, and timing. Repeat the same call in `curl -v`.
  **Point out:** it is the same conversation, three different views.
- **Ask:**
  - Q: Which curl flag shows the headers you sent and got? — A: `-v` (verbose); `-i` shows response headers.
- **Done when:** every candidate has opened the Network tab once.

---

## Exercise (candidates, ~15 min)
Write five `curl` commands against the HR API: list employees of department 2, fetch one employee, create one, update its title, delete it. Show the status code of each. Stretch: make each of 404, 405, 409 and 422 happen on purpose.

## Done-check (instructor asks the room; agent records the result)
1. Read a raw request and name its parts.
2. Pick method and status for: create, read, replace, partial update, delete.
3. Explain stateless, and idempotent vs safe.
4. Name five headers.
5. Describe a 304 round trip.

## Clean-up
`scripts/setup.sh --reset` restores seed data if the demos left stray records.
