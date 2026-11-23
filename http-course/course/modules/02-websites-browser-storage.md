# Module 2 — Websites, Browser and Storage

Teach-skill content file (format: `.claude/skills/teach-http-class/SKILL.md`). All demos in this module run on the current stack (`scripts/setup.sh` starts the web page on :3000 and the API on :8000; verified in a real browser).
Time: about 90 minutes.

## Objectives
Explain what happens between typing a URL and seeing a page; describe a page as HTML, CSS and JS; show how a page calls an API; use cookies, `localStorage` and `sessionStorage` correctly; explain same-origin policy and fix a CORS error.

## Stack requirements
`scripts/setup.sh` READY (web page `http://localhost:3000`, API `http://localhost:8000`). **Start the module with CORS off**, which is the default; if a previous run left it on, run `docker compose up -d` to turn it off. Cookies are scoped to the host, not the port, so a cookie set by `:8000` is also visible to the page on `:3000`.

---

### Beat 2.1 — What happens when you type a URL
- **Slides:** NEW slide: "From URL to pixels: DNS → TCP → TLS → request → response → render"
- **Say:**
  - Browser checks cache and HSTS, resolves the name (DNS: resolver → root → TLD → authoritative, with a TTL), opens TCP, does the TLS handshake, sends the request, gets the response, then renders.
  - Each phase has a cost; the waterfall in DevTools shows them.
- **Demo (run: agent):** timings for each phase.
  ```bash
  curl -s -o /dev/null -w "dns %{time_namelookup}s | connect %{time_connect}s | tls %{time_appconnect}s | first byte %{time_starttransfer}s | total %{time_total}s\n" https://example.com
  ```
  **Point out:** the numbers are cumulative; tls minus connect is the handshake cost; first byte is server think time plus travel.
- **Demo (run: instructor):** open any page, DevTools → Network, reload, show the waterfall (DNS, connect, TLS, waiting, download).
- **Ask:**
  - Q: Put these in order: TLS handshake, DNS lookup, TCP connect, send request. — A: DNS, TCP, TLS, send request.
  - Q: Why can the second visit be faster? — A: DNS and HTTP caches, reused connections.
- **Done when:** they can narrate the sequence.

### Beat 2.2 — Anatomy of a page
- **Slides:** NEW slide: "HTML, CSS, JS and the DOM; static vs SSR vs SPA"
- **Say:**
  - HTML = structure, CSS = presentation, JS = behavior. The browser parses HTML into the DOM tree; each image, script and stylesheet is another request.
  - Static: files served as-is. Server-rendered: server builds HTML per request. SPA: one shell, JS fetches data and builds the DOM.
- **Demo (run: agent):**
  ```bash
  curl -s https://example.com | head -c 700; echo
  ```
  **Point out:** that is "View Source": the HTML the server sent, before any JS (it is minified onto one line, which is why we cut it at 700 characters).
- **Demo (run: instructor):** Elements panel vs View Source on a JS-heavy site: the DOM differs from the source because JS changed it.
- **Ask:**
  - Q: View Source vs the Elements panel: why different? — A: Source is what the server sent; Elements is the live DOM after JS ran.
  - Q: What is one tradeoff of an SPA? — A: Slower first paint and SEO work, in return for fast in-app navigation.
- **Done when:** they can classify a site as static, server-rendered or SPA.

### Beat 2.3 — A page calls an API
- **Slides:** NEW slide: "fetch/AJAX: page → API → JSON → DOM"; also web server vs app server vs reverse proxy, CDN
- **Say:**
  - JavaScript calls `fetch(url)`, gets JSON, and updates the DOM. This is how every modern app talks to an API.
  - nginx serves static files and proxies; uvicorn runs our Python app. A CDN caches static files near users; compression and lazy loading cut load time.
- **Demo (run: instructor):** open `http://localhost:3000`, DevTools → Network → filter Fetch/XHR, reload. Show the `GET /v2/employees` request and the JSON preview, then the list rendered in the page.
- **Demo (run: agent):**
  ```bash
  curl -sI http://localhost:3000 | head -5
  curl -sI http://localhost:8000/v2/employees | head -5
  ```
  **Point out:** two servers, two ports: static page vs API.
- **Ask:**
  - Q: Where does the HTML come from, and where does the data come from? — A: HTML and JS from the web server (:3000); data from the API (:8000).
  - Q: What does a CDN do? — A: Caches static content at the edge, closer to users.
- **Done when:** they can draw page → API → JSON → DOM.

### Beat 2.4 — Cookies and sessions
- **Slides:** 15 · NEW slides: "Cookie attributes", "Sessions"
- **Say:**
  - Server sends `Set-Cookie`; browser sends `Cookie` back on every matching request. That is how stateless HTTP remembers you.
  - Attributes: `Domain`, `Path`, `Max-Age`/`Expires`, `Secure` (HTTPS only), `HttpOnly` (JS cannot read), `SameSite` (Strict/Lax/None: cross-site sending). About 4 KB each, sent on every request.
  - Session: cookie holds an ID, data stays on the server. First-party vs third-party cookies; tracking and consent.
- **Demo (run: agent):**
  ```bash
  curl -si -c /tmp/jar.txt http://localhost:8000/demo/cookie | grep -i '^set-cookie'
  curl -s -b /tmp/jar.txt http://localhost:8000/demo/whoami
  curl -s http://localhost:8000/demo/whoami
  ```
  **Point out:** two `set-cookie` lines with different attributes (`session_id` is `HttpOnly`, `theme` has a `Max-Age`); with the jar the server sees both cookies, without it the server sees none.
- **Demo (run: instructor):** on `http://localhost:3000` click "Set demo cookies (opens API)", then DevTools → Application → Cookies → `http://localhost:8000` (cookies are per host, so also visible for `localhost`): see the flags. In the console, `document.cookie` shows only `theme=dark`; the `HttpOnly` `session_id` is absent, yet the server still receives it (try `curl`-free: `fetch('http://localhost:8000/demo/whoami',{credentials:'include'}).then(r=>r.json())` once CORS is on).
- **Ask:**
  - Q: What does `HttpOnly` protect against? — A: Scripts (XSS) reading the cookie.
  - Q: What does `SameSite` protect against? — A: Cross-site requests sending the cookie (CSRF).
  - Q: Why is a session ID better than storing data in the cookie? — A: Small, can't be tampered with, data stays on the server.
- **Done when:** they can describe the Set-Cookie / Cookie round trip.

### Beat 2.5 — Browser storage
- **Slides:** NEW slide: "localStorage, sessionStorage, IndexedDB, Cache API; comparison table"
- **Say:**
  - `localStorage` persists per origin (~5 MB, strings, synchronous); `sessionStorage` lasts for the tab; IndexedDB is larger structured storage; Cache API pairs with service workers.
  - None of them is sent to the server automatically (unlike cookies). Any script on the page can read them.
  - What goes where: theme or last filter → localStorage; form draft → sessionStorage; session ID → HttpOnly cookie. Never passwords or salary data.
- **Demo (run: instructor):** in the console on `http://localhost:3000`:
  ```js
  localStorage.setItem('theme', 'dark'); localStorage.getItem('theme');
  sessionStorage.setItem('draft', 'half-written note');
  ```
  Reload; open a new tab; show Application → Storage. localStorage survives, sessionStorage is per tab.
- **Ask:**
  - Q: Which storage is sent to the server automatically? — A: Cookies only.
  - Q: Why not keep a login token in localStorage? — A: Any injected script can read it (XSS); we revisit this in Modules 4–5.
- **Done when:** they can pick the right storage for three examples.

### Beat 2.6 — Same-origin policy and CORS
- **Slides:** NEW slide: "Origin, same-origin policy, CORS and preflight"
- **Say:**
  - Origin = scheme + host + port. `:3000` and `:8000` are different origins, so the browser blocks the page from reading the API's response unless the API opts in.
  - The API opts in with `Access-Control-Allow-Origin` (+ `-Methods`, `-Headers`, `-Credentials`). Non-simple requests trigger a **preflight** `OPTIONS` first.
  - CORS is enforced by the browser only; `curl` ignores it. It is not authentication.
- **Demo (run: instructor):** with CORS off the page says "Could not load employees (Failed to fetch)". The Console shows "blocked by CORS policy: No 'Access-Control-Allow-Origin' header is present"; the Network row is red (`net::ERR_FAILED`) even though the server answered 200 (the agent proves that with `curl` below).
- **Demo (run: agent):** show the header on the server side.
  ```bash
  curl -si -H "Origin: http://localhost:3000" http://localhost:8000/v2/employees/1 | grep -i "^HTTP\|access-control"
  docker compose -f docker-compose.yml -f docker-compose.cors.yml up -d   # wait ~5s for the API to restart
  curl -si -H "Origin: http://localhost:3000" http://localhost:8000/v2/employees/1 | grep -i "^HTTP\|access-control"
  curl -si -X OPTIONS http://localhost:8000/v2/employees/1 -H "Origin: http://localhost:3000" -H "Access-Control-Request-Method: PUT" | grep -i "^HTTP\|access-control"
  ```
  **Point out:** first call: HTTP 200 and no `access-control-allow-origin` (the server answered, the browser refuses to expose it); after enabling CORS it echoes `http://localhost:3000` and adds `access-control-allow-credentials: true`; the preflight answers with `access-control-allow-methods` and `access-control-max-age`. A different origin (`-H "Origin: http://evil.example"`) gets no allow-origin header. Then reload the page: all 20 employees appear.
- **Ask:**
  - Q: Why did curl work but the browser fail? — A: CORS is enforced by browsers, not servers.
  - Q: What are the three parts of an origin? — A: Scheme, host, port.
  - Q: Why a preflight? — A: To ask the server whether a non-simple cross-origin request is allowed before sending it.
- **Done when:** they can explain the error and the fix.

### Beat 2.7 — Briefly: WebSockets, SSE, consent, SEO (no demo)
- **Slides:** NEW slide (one slide, bullets)
- **Say:** WebSockets and Server-Sent Events: real-time over HTTP, appendix material. Cookie consent and GDPR exist; SEO and sitemaps are out of scope.
- **Done when:** the names are familiar.

---

## Exercise (candidates, ~20 min)
Add a "department" filter to the directory page that remembers the last choice across reloads, and call `GET /v2/employees?department_id=N`. Then explain, in two sentences, why you stored it where you did.

## Done-check
1. Narrate URL → page in order.
2. Explain View Source vs DOM.
3. Explain HttpOnly, Secure, SameSite.
4. Choose cookie vs localStorage vs sessionStorage for three cases.
5. Explain a CORS error and its fix.

## Clean-up
`docker compose up -d` (CORS back off); `scripts/setup.sh --reset` if data changed; clear the page's storage in DevTools → Application → Clear site data.
