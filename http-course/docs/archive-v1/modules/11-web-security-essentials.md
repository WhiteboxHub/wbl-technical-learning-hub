# Module 11 — Web Security Essentials (detailed TOC, draft v1)

All new, building on Modules 2, 3, 9, 10.

## 11.1 Where to store tokens in the browser
- localStorage, sessionStorage, in-memory, HttpOnly cookie
- Trade-offs: XSS can read the first three, CSRF affects cookies
- Recommended patterns (HttpOnly + SameSite cookie, or in-memory + refresh cookie)

## 11.2 XSS (cross-site scripting)
- Stored, reflected, DOM-based
- Demo: an employee "notes" field that runs a script
- Defenses: output encoding, CSP, sanitization, HttpOnly

## 11.3 CSRF (cross-site request forgery)
- Browser sends cookies automatically
- Demo: a hostile page triggers `DELETE /employees/5`
- Defenses: SameSite, CSRF tokens, custom headers, Origin checks

## 11.4 CORS as a security control
- What it does and does not protect (recap of 2.7)
- Credentials and wildcards

## 11.5 Injection
- SQL injection with the HR search endpoint
- Parameterized queries/ORM, input validation, allow-lists

## 11.6 OWASP API Security Top 10 (highlights)
- Broken object-level authorization (read someone else's `/employees/{id}`)
- Broken authentication, excessive data exposure (salary leak)
- Lack of rate limiting, mass assignment, security misconfiguration

## 11.7 Transport security
- TLS certificates, expiry, self-signed in dev, HSTS (recap of 1.12)
- Secure cookie flag

## 11.8 Security headers
- `Content-Security-Policy`, `X-Content-Type-Options`, `X-Frame-Options`, `Strict-Transport-Security`, `Referrer-Policy`

## 11.9 Secrets and configuration
- Environment variables, no secrets in git, rotation
- `.env` and Docker secrets in the lab

## 11.10 Validation and error handling
- Validate on the server, always
- Don't leak internals in errors

## Labs
1. Exploit the vulnerable endpoint (XSS, then SQL injection), then fix it
2. Forge a cross-site request, then block it with SameSite
3. Find the BOLA bug in a given endpoint
4. Candidate exercise: run a security checklist against their own HR API

## Candidate question bank (sample)
- XSS vs CSRF?
- Why is localStorage risky for tokens?
- What is BOLA and how do you prevent it?

## Slide work
- **Add:** about 12 slides (new module). Vulnerable demo app lives in the setup repo
