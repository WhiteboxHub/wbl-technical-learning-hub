# Module 2 — Websites and the Browser (detailed TOC, draft v1)

Status: **Have** · **Thin** · **Add**. All of this module is new. Slides 8 and 17 touch the edges only.

## 2.1 What happens when you type a URL
- Browser parses URL, checks HSTS and cache
- DNS lookup (resolver, recursive, root/TLD/authoritative, TTL)
- TCP connection, TLS handshake, HTTP request, response, render
- Timeline view in DevTools (DNS, connect, TLS, TTFB, download)
**Add** · Demo: Network tab waterfall for one page load

## 2.2 Anatomy of a web page
- HTML (structure), CSS (presentation), JavaScript (behavior)
- DOM tree, how the browser builds it
- Sub-resources: images, scripts, stylesheets, fonts, each its own request
- View Source vs Elements panel
**Add**

## 2.3 Rendering and page types
- Static site, server-rendered (SSR), single-page app (SPA), hybrid
- Where HTML is generated and what that means for requests
- Client-side vs server-side routing
**Add** · Demo: same HR directory as static, SSR and SPA, compared in the Network tab

## 2.4 How a page talks to an API
- `fetch` and `XMLHttpRequest`, AJAX history
- JSON response → update DOM
- Loading, error and empty states
- HR directory page calling `GET /employees`
**Add**

## 2.5 Web servers and where code runs
- Web server vs application server vs reverse proxy (nginx, uvicorn)
- Static files vs dynamic responses
- Frontend app vs backend API, and the browser/server boundary
**Add**

## 2.6 CDN and performance basics
- What a CDN does, edge caching, cache headers (link to 1.13)
- Compression, minification, lazy loading
- HTTP/2 effect on number of requests
- Core Web Vitals in one slide
**Add**

## 2.7 Same-origin policy and CORS
- Origin = scheme + host + port
- What the browser blocks and why
- Simple vs preflighted requests, `OPTIONS`
- `Origin`, `Access-Control-Allow-Origin`, `-Methods`, `-Headers`, `-Credentials`
- Common mistakes (`*` with credentials)
**Add** · Demo: page on `:3000` calls API on `:8000`, see the error, fix it in FastAPI

## 2.8 Web vs native and other web basics
- Browser vs mobile app, both calling the same API
- Web sockets and SSE (one slide, pointer to appendix)
- Robots, sitemaps, SEO (one slide, optional)
**Add** (Stretch)

## Labs
1. Record a page load; label each phase in the waterfall
2. Find and name every request one page makes
3. Build the HR directory page with `fetch`
4. Cause and fix a CORS error
5. Candidate exercise: add a department filter to the page

## Candidate question bank (sample)
- What happens between pressing Enter and seeing the page?
- Why does a CORS error appear in the browser but not in curl?
- Static vs SSR vs SPA: when would you pick each?
- What is an origin?

## Slide work
- **Add:** all of 2.1–2.7 (about 14 slides, two diagrams)
