# Module 5 — SSO and Web Security

Teach-skill content file. All demos run on the current stack. Verified live: Keycloak discovery and keys, the full code + PKCE login in a real browser, SSO across two apps, local vs IdP logout, API validation of Keycloak tokens, and the three exploits against the vulnerable app.
Time: about 2 hours (split after Beat 5.6).

## Objectives
Explain why SSO exists and how OAuth 2.0 authorization code with PKCE and OIDC work; follow a login through its redirects; show one login working across two apps; describe logout and MFA; store tokens safely in a browser; recognize and fix XSS, CSRF and SQL injection.

## Stack requirements
- Start Keycloak and the two SSO apps (optional profile; first start takes ~15 s, the first image pull longer): `docker compose --profile sso up -d --build`. Keycloak: `http://localhost:8081` (realm `hr`), portal `http://localhost:3001`, payroll `http://localhost:3002`.
- Users `hr_admin`, `manager`, `employee`; the password is the same dev-only demo password as Module 4. Read it privately with `docker compose exec -T api printenv DEMO_PASSWORD`; never show it on screen.
- The vulnerable app runs by default on `http://localhost:3003` (in-memory data; `docker compose restart vuln` resets it). Evil page: `http://localhost:3000/evil.html`.
- Beat 5.6 needs the API to trust Keycloak: `docker compose --profile sso -f docker-compose.yml -f docker-compose.oidc.yml up -d`. Afterwards `docker compose --profile sso up -d --force-recreate api` returns to the default.

---

### Beat 5.1 — Why SSO
- **Slides:** NEW slide: "The password problem; IdP and relying party"
- **Say:** many apps (HR portal, payroll, benefits, timesheets) × many passwords = fatigue, reuse, helpdesk load, slow offboarding. SSO: one identity provider (IdP) authenticates the user; each app (relying party) trusts it. Offboarding one account removes access everywhere.
- **Ask:**
  - Q: Who authenticates the user in SSO? — A: The IdP, not each app.
  - Q: One security benefit for offboarding? — A: Disable one account to cut off every app.
- **Done when:** they can name IdP and relying party in the HR example.

### Beat 5.2 — OAuth 2.0 grants
- **Slides:** NEW slide: "Grant types: authorization code + PKCE, client credentials, device code; why implicit and password are out"
- **Say:** authorization code + PKCE for web, SPA and mobile (recommended). Client credentials for service-to-service. Device code for TVs and CLIs. Implicit and resource-owner-password are deprecated: tokens in URLs, passwords shared with apps.
- **Ask:**
  - Q: Which grant for a backend service calling another service? — A: Client credentials.
  - Q: Why was the password grant dropped? — A: The app sees the user's password, defeating OAuth's purpose.
- **Done when:** they can pick a grant for three cases.

### Beat 5.3 — Authorization code + PKCE step by step
- **Slides:** NEW slide(s): sequence diagram
- **Say:**
  1. App redirects the browser to the IdP with `client_id`, `redirect_uri`, `scope`, `state`, `code_challenge`.
  2. User logs in and consents at the IdP.
  3. IdP redirects back with a short-lived `code` (and the same `state`).
  4. App's backend (or SPA) exchanges `code` + `code_verifier` for tokens.
  5. App calls the API with the access token.
  - `state` blocks CSRF on the callback; PKCE blocks a stolen `code` from being redeemed.
- **Demo (run: agent):** the IdP's published configuration.
  ```bash
  curl -s http://localhost:8081/realms/hr/.well-known/openid-configuration | python3 -m json.tool | grep -E '"(issuer|authorization_endpoint|token_endpoint|jwks_uri|userinfo_endpoint)"'
  ```
  **Point out:** every endpoint a client needs is discoverable from one URL.
- **Demo (run: instructor):** DevTools → Network with "Preserve log", open `http://localhost:3001`, click Login. Walk the redirects: app → `/auth` (with `code_challenge`) → login form → back to app with `?code=…&state=…` → token request.
- **Ask:**
  - Q: What is the `state` parameter for? — A: Ties the response to the request; blocks CSRF on the callback.
  - Q: What does PKCE protect against? — A: A stolen authorization code being used by someone else.
- **Done when:** they can narrate the five steps.

### Beat 5.4 — OIDC
- **Slides:** NEW slide: "OIDC = OAuth + identity"
- **Say:** OAuth gives access; OIDC adds authentication. The **ID token** (a JWT) says who logged in (`sub`, `email`, `name`); the **access token** is for calling APIs. `openid` scope, discovery document, JWKS for verifying signatures, `/userinfo` for profile data.
- **Demo (run: agent):** fetch the signing keys.
  ```bash
  curl -s http://localhost:8081/realms/hr/protocol/openid-connect/certs | python3 -m json.tool | head -15
  ```
  **Point out:** public keys with a `kid`; the API verifies tokens with these and never needs a shared secret. Decode an ID token as in Module 4 Beat 4.5.
- **Ask:**
  - Q: ID token vs access token? — A: ID token = who logged in (for the app); access token = permission to call an API.
  - Q: How does the API verify a token without talking to the IdP each time? — A: Checks the signature using the cached public keys (JWKS).
- **Done when:** they can say which token goes where.

### Beat 5.5 — SSO in action, logout, MFA
- **Slides:** NEW slide(s): "SSO session, single logout, MFA, SAML in one slide"
- **Say:** the IdP keeps its own session cookie; when app B redirects to the IdP, the IdP sees the session and returns a code immediately: no password prompt. Logout is hard: local logout ≠ IdP logout ≠ logout everywhere (single logout needs front/back-channel calls). MFA: something you know, have, are (TOTP, passkeys). Step-up: ask for MFA again before viewing salaries. SAML: older XML-based SSO common in enterprises; same idea, different format.
- **Demo (run: instructor):** log in at `http://localhost:3001` (portal; the instructor types `hr_admin` and the demo password). Open `http://localhost:3002/login` (payroll) in the same browser: **no login prompt**, you land signed in. Click "show tokens' claims" to read the ID and access tokens. On the portal click **local logout**, then reload payroll: still signed in (each app has its own session). Now on payroll click **logout everywhere (IdP)**, then open `http://localhost:3001/login`: the Keycloak login form appears again because the SSO session is gone.
- **Ask:**
  - Q: Why no second password prompt? — A: The IdP session cookie proves the user already authenticated.
  - Q: Why does logging out of one app not log out the others? — A: Each app has its own session; only IdP or single logout ends them all.
- **Done when:** they can explain SSO and why logout is hard.

### Beat 5.6 — Protecting the HR API with the IdP
- **Slides:** NEW slide: "API validates IdP tokens; map groups to roles"
- **Say:** the API checks signature (via JWKS), `exp`, `iss`, `aud`; maps IdP roles/groups to API roles; the earlier salary rules (Module 4) now use IdP claims.
- **Demo (run: agent):** switch the API to trust Keycloak, then call it with Keycloak-issued tokens (the password grant is used here only so a CLI can get a token; real apps use the code flow you just saw).
  ```bash
  docker compose --profile sso -f docker-compose.yml -f docker-compose.oidc.yml up -d   # wait ~5s
  PW=$(docker compose exec -T api printenv DEMO_PASSWORD)
  for u in manager employee; do
    T=$(curl -s -X POST http://localhost:8081/realms/hr/protocol/openid-connect/token -d grant_type=password -d client_id=hr-api-cli -d "username=$u" --data-urlencode "password=$PW" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")
    echo "$u: employee 7 -> $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $T" localhost:8000/v2/employees/7)  employee 1 -> $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $T" localhost:8000/v2/employees/1)  tampered -> $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer ${T%?}X" localhost:8000/v2/employees/7)"
  done
  ```
  **Point out:** the same bearer mechanism and the same role rules as Module 4, but the token now comes from Keycloak and the API checks its signature with the realm's public keys (JWKS). Expected: `200`, `403`, `401` for both users. Then in the browser open `http://localhost:3002/api` while signed in: the app calls the API with its own access token and shows `200` and Sofia Rossi's record.
- **Ask:**
  - Q: What does the API trust? — A: The IdP's signature, `iss` and `aud`, not the client's claims.
- **Done when:** they can say who issues the token and who checks it.

### Beat 5.7 — Where to keep tokens in the browser
- **Slides:** NEW slide: comparison table
- **Say:** `localStorage` and `sessionStorage` are readable by any script (XSS risk). An `HttpOnly` cookie is invisible to scripts but sent automatically (CSRF risk, mitigated by `SameSite` and tokens). In-memory plus a refresh cookie is a common compromise. There is no free lunch: choose the threat you can defend.
- **Ask:**
  - Q: Which storage risks XSS theft? Which risks CSRF? — A: localStorage/sessionStorage → XSS; cookies → CSRF.
- **Done when:** they can recommend one pattern and defend it.

### Beat 5.8 — Attacks and defenses
- **Slides:** NEW slides: XSS, CSRF, injection, OWASP API Top 10, security headers
- **Say:**
  - **XSS:** untrusted input runs as script in another user's page. Defend with output encoding, CSP, sanitizing, `HttpOnly`.
  - **CSRF:** a hostile site makes the browser send your cookie to the API. Defend with `SameSite`, CSRF tokens, `Origin` checks.
  - **SQL injection:** input becomes SQL. Defend with parameterized queries or an ORM, and validation.
  - **BOLA** (broken object-level authorization): changing an ID in the URL reads someone else's record. Check ownership on every request.
  - Also: excessive data exposure (salary), mass assignment, missing rate limits, secrets in git, expired TLS certificates.
  - Security headers: `Content-Security-Policy`, `X-Content-Type-Options`, `Strict-Transport-Security`, `Referrer-Policy`.
- **Demo (run: instructor):** on `http://localhost:3003` (the banner shows VULNERABLE or FIXED; the "switch" link toggles `?fixed=1`).
  1. **XSS:** open *notes*, add `<img src=x onerror=alert(1)>`: the alert fires for anyone who views the page. In FIXED mode the same note shows as plain text.
  2. **CSRF:** click "Log in as hr_admin", then open `http://localhost:3000/evil.html` (a different origin) and press "Show me the cats": employee 4 is deleted using your cookie. Use "same attack against the FIXED app": it is refused (`403`, bad Origin / missing CSRF token). *Teaching note:* browsers treat `localhost:3000` and `localhost:3003` as the **same site** (ports don't count), so `SameSite=Lax` would not have saved us here; the fix is an Origin check plus a CSRF token.
  3. **SQL injection:** in *search*, enter `' OR '1'='1`: every employee, with salary, comes back. In FIXED mode: "no match".
  Reset the data afterwards with `docker compose restart vuln`.
- **Demo (run: agent):** show each fix as code in `vuln/app.py`: `html.escape` on output (XSS), the `Origin` and `csrf` checks in `delete()` (CSRF), and `WHERE name = ?` with a parameter instead of string formatting (SQL injection). Prove each from the command line:
  ```bash
  V=http://localhost:3003
  curl -s -X POST $V/notes -d 'text=<img src=x onerror=alert(1)>' -o /dev/null; curl -s $V/notes | grep -o "<li><img[^>]*>"
  curl -s "$V/notes?fixed=1" | grep -o "<li>&lt;img[^<]*"
  curl -s -G $V/search --data-urlencode "q=' OR '1'='1" | grep -o "<td>[A-Za-z ]*</td>" | head -3
  curl -s -X POST $V/delete -H "Cookie: session=hr_admin" -H "Origin: http://localhost:3000" -d id=6 -o /dev/null -w "vulnerable CSRF: %{http_code}\n"
  curl -s -X POST "$V/delete?fixed=1" -H "Cookie: session=hr_admin" -H "Origin: http://localhost:3000" -d id=5 -w " -> %{http_code}\n"
  docker compose restart vuln
  ```
- **Ask:**
  - Q: XSS vs CSRF in one sentence each? — A: XSS runs attacker script in your page; CSRF makes your browser send an authenticated request you didn't intend.
  - Q: What is BOLA and the simplest defense? — A: Accessing other users' objects by ID; check ownership server-side on every request.
- **Done when:** they can name an attack, its cause and its fix, three times.

---

## Exercise (candidates, ~30 min)
1. Log in at the portal, open payroll, and write down every redirect and cookie that made the second login unnecessary.
2. Fix one vulnerability in `vuln/` (their choice) and prove the fix with a request.
3. Stretch: add a third app to the Keycloak realm.

## Done-check
1. Narrate the code + PKCE flow.
2. Say what is in an ID token vs an access token.
3. Explain why SSO needs no second password and why logout is hard.
4. Recommend a browser token storage and defend it.
5. Identify XSS, CSRF, SQLi and BOLA from a description.

## Clean-up
`scripts/setup.sh --reset`; stop the `keycloak`, `portal`, `payroll` and `vuln` services if they were started separately.
