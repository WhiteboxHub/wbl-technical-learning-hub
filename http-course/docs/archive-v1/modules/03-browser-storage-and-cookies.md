# Module 3 — Browser Storage and Cookies (detailed TOC, draft v1)

Status: **Have** (slide 15 only) · **Thin** · **Add**

## 3.1 Why browsers store data
- HTTP is stateless (link to 1.14)
- Use cases: login state, preferences, cart, offline data, caching
**Thin** (slide 15)

## 3.2 Cookies in depth
- `Set-Cookie` / `Cookie` round trip
- Attributes: Domain, Path, Expires/Max-Age, Secure, HttpOnly, SameSite (Strict, Lax, None)
- Session vs persistent cookies
- First-party vs third-party, tracking, consent banners
- Size limit (~4 KB) and sent on every request
**Thin** · Demo: set, inspect, expire and delete a cookie

## 3.3 Sessions
- Server-side session: session ID in a cookie, data on the server
- Session stores (memory, DB, Redis)
- Session fixation and expiry
**Add**

## 3.4 Web Storage: localStorage and sessionStorage
- API: `setItem`, `getItem`, `removeItem`, `clear`
- Scope: per origin; sessionStorage per tab
- ~5 MB, strings only, synchronous, **not sent to the server**
- Readable by any script on the page (XSS exposure)
**Add** · Demo: DevTools Application tab

## 3.5 IndexedDB and the Cache API
- Larger structured client storage, async
- Cache API with service workers, offline pages (overview)
**Add** (Stretch)

## 3.6 Comparison table
| | Cookie | localStorage | sessionStorage | IndexedDB |
|---|---|---|---|---|
| Sent to server | yes | no | no | no |
| Size | ~4 KB | ~5 MB | ~5 MB | large |
| Lifetime | configurable | until cleared | tab | until cleared |
| JS access | unless HttpOnly | yes | yes | yes |
**Add**

## 3.7 What goes where (HR examples)
- Theme, language, last department filter → localStorage
- Session ID → HttpOnly cookie
- Form draft → sessionStorage
- Never: passwords, salary data, long-lived secrets

## 3.8 Tokens in the browser (setup for Modules 9–11)
- Token in HttpOnly cookie vs localStorage vs memory
- XSS vs CSRF trade-offs (detail in Module 11)
**Add**

## 3.9 Privacy and regulation
- Cookie consent, GDPR/CCPA at awareness level
**Add** (Stretch)

## Labs
1. Inspect the Set-Cookie header from the HR login endpoint
2. Add and read each storage type from the console
3. Flip HttpOnly and show that `document.cookie` can no longer read it
4. Candidate exercise: remember the department filter across reloads

## Candidate question bank (sample)
- Cookie vs localStorage: which is sent to the server?
- What does HttpOnly protect against? What does SameSite protect against?
- Why is localStorage risky for tokens?

## Slide work
- **Thin:** extend slide 15 into 3 slides
- **Add:** 3.3–3.8 (about 8 slides, one comparison table)
