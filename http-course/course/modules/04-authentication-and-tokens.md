# Module 4 — Authentication and Tokens

Teach-skill content file. All demos run on the current stack (verified live with auth on, plus 9 auth pytest tests).
Time: about 90 minutes.

## Objectives
Distinguish authentication from authorization (401 vs 403); explain Basic, API key and bearer auth; read a JWT and validate it; explain token lifetime and refresh; implement role-based access so the same endpoint returns different data to different users.

## Stack requirements
Start with auth on: `docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d` (wait ~5s). Users: `hr_admin` (Priya Raman, employee 1), `manager` (Marcus Lee, employee 2, Engineering) and `employee` (Sofia Rossi, employee 7, Engineering). Get tokens with the helper, which reads the dev-only demo password from the running API so you never type or show it:
```bash
HR=$(scripts/token.sh hr_admin); MGR=$(scripts/token.sh manager); EMP=$(scripts/token.sh employee)
```
Rules the API enforces: `hr_admin` reads and writes everything; `manager` reads only their own department (list and single records) and cannot write; `employee` reads only their own record and cannot write; departments are readable by anyone logged in. Return to normal afterwards with `docker compose up -d`.

---

### Beat 4.1 — Authentication vs authorization
- **Slides:** 62
- **Say:** authentication = who are you; authorization = what may you do. Unauthenticated → **401**; authenticated but not allowed → **403**.
- **Demo (run: agent):**
  ```bash
  curl -s -o /dev/null -w "no token: %{http_code}\n" http://localhost:8000/v2/employees/7
  curl -s -o /dev/null -w "bad token: %{http_code}\n" -H "Authorization: Bearer nonsense" http://localhost:8000/v2/employees/7
  curl -s -o /dev/null -w "employee reads another's record: %{http_code}\n" -H "Authorization: Bearer $EMP" http://localhost:8000/v2/employees/2
  ```
  **Point out:** 401, 401, then 403.
- **Ask:**
  - Q: 401 or 403: valid login, wrong permission? — A: 403.
  - Q: 401 or 403: no credentials at all? — A: 401.
- **Done when:** they sort five scenarios into 401/403.

### Beat 4.2 — Basic, API key, bearer
- **Slides:** 61, 64 · NEW slide: "Bearer tokens; password hashing"
- **Say:**
  - **Basic:** `Authorization: Basic base64(user:pass)`. Base64 is encoding, not encryption: HTTPS only. Credentials go with every request; no logout.
  - **API key:** identifies an application, not a person; keep it in a header, never in a URL; rotate it.
  - **Bearer:** `Authorization: Bearer <token>`; whoever holds the token is the user.
  - Never store plaintext passwords: hash with bcrypt or argon2, salted.
- **Demo (run: agent):** decode Basic by hand.
  ```bash
  echo -n 'demo-user:demo-pass' | base64
  echo 'ZGVtby11c2VyOmRlbW8tcGFzcw==' | base64 -d; echo
  ```
  **Point out:** anyone who sees the header can read it. (These are dummy values, not credentials.)
- **Demo (run: agent):**
  ```bash
  curl -si http://localhost:8000/demo/basic | grep -iE "^HTTP|^www-authenticate"
  PW=$(docker compose exec -T api printenv DEMO_PASSWORD)
  curl -s -u "hr_admin:$PW" http://localhost:8000/demo/basic
  ```
  **Point out:** without credentials: `401` and `www-authenticate: Basic realm=...`; with `-u`, curl adds the `Authorization: Basic ...` header you decoded above. (Do not display `$PW`.)
- **Ask:**
  - Q: Is Base64 encryption? — A: No, it is reversible encoding.
  - Q: Why shouldn't an API key go in the URL? — A: URLs end up in logs, history and referrers.
- **Done when:** they can decode a Basic header.

### Beat 4.3 — OAuth 2.0 concepts
- **Slides:** 65, 66
- **Say:** OAuth lets an app act for a user without getting their password. Roles: resource owner, client, authorization server, resource server. Tokens: access (short-lived), refresh (long-lived); scopes say what is allowed. OAuth 1.0 signed requests; 2.0 uses bearer tokens over TLS.
- **Ask:**
  - Q: What problem does OAuth solve? — A: Delegated access without sharing the password.
  - Q: Who issues the token? — A: The authorization server.
- **Done when:** they can name the four roles.

### Beat 4.4 — Sessions vs tokens
- **Slides:** NEW slide: "Session cookie vs token"
- **Say:** session: ID in a cookie, data on the server (easy to revoke, needs shared storage to scale). Token: self-contained, stateless, scales easily, harder to revoke. Cookies suit browsers; tokens suit APIs and mobile.
- **Ask:**
  - Q: Which is easier to revoke immediately? — A: A server-side session.
  - Q: Which scales more easily across servers? — A: Self-contained tokens.
- **Done when:** they can give one pro and con of each.

### Beat 4.5 — JWT
- **Slides:** NEW slides: "JWT anatomy", "Signing"
- **Say:**
  - Three Base64URL parts: header, payload, signature. Registered claims: `iss`, `sub`, `aud`, `exp`, `iat`; ours add `role` and `dept`.
  - **Signed ≠ encrypted**: anyone can read the payload; only the key holder can produce a valid signature. Never put secrets in it.
  - HS256 shared secret vs RS256/ES256 key pair (public key verifies). Reject `alg: none`.
- **Demo (run: agent):** get and decode a token.
  ```bash
  curl -s -X POST http://localhost:8000/v2/auth/token -d "username=hr_admin" --data-urlencode "password=$(docker compose exec -T api printenv DEMO_PASSWORD)" | python3 -m json.tool | cut -c1-110
  scripts/jwt-decode.py "$HR"
  ```
  **Point out:** header (`alg`, `typ`), payload (`sub`, `role`, `exp`). Anyone can do this decode, so no secrets inside. Paste the token into jwt.io to see the same.
- **Ask:**
  - Q: Can the client read the payload? Can it change it? — A: Yes; changing it breaks the signature.
  - Q: What does `exp` do? — A: Tells the server when to stop accepting the token.
- **Done when:** they can name the three parts and what each holds.

### Beat 4.6 — Token lifecycle
- **Slides:** NEW slide: "Expiry, refresh, revocation, validation"
- **Say:** short-lived access tokens limit damage; a refresh token gets a new one; rotate refresh tokens. Validation checklist: signature, `exp`, `iss`, `aud`. Revocation of stateless tokens is hard: short expiry, a blocklist, or token versions.
- **Demo (run: agent):** tamper and expiry.
  ```bash
  curl -s -o /dev/null -w "valid: %{http_code}\n"  -H "Authorization: Bearer $TOKEN" http://localhost:8000/v2/employees/7
  BAD="${TOKEN%?}X"
  curl -s -o /dev/null -w "tampered: %{http_code}\n" -H "Authorization: Bearer $BAD" http://localhost:8000/v2/employees/7
  ```
  Then expiry with 5-second tokens:
  ```bash
  TOKEN_TTL=5 docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d   # wait ~5s for the API
  T=$(scripts/token.sh hr_admin); curl -s -o /dev/null -w "fresh: %{http_code}\n" -H "Authorization: Bearer $T" http://localhost:8000/v2/employees/7
  sleep 6; curl -s -w " -> %{http_code}\n" -H "Authorization: Bearer $T" http://localhost:8000/v2/employees/7
  docker compose -f docker-compose.yml -f docker-compose.auth.yml up -d               # back to 15-minute tokens
  ```
  **Point out:** valid 200, tampered 401, and after 6 seconds `{"detail":"token expired"}` 401.
- **Ask:**
  - Q: Why short access-token lifetimes? — A: A stolen token is only useful briefly.
  - Q: Name three things to check when validating a JWT. — A: Signature, expiry, issuer/audience.
- **Done when:** they can describe the refresh flow.

### Beat 4.7 — Authorization: roles, scopes, ownership
- **Slides:** NEW slide: "RBAC, scopes, ownership"
- **Say:** RBAC: roles map to permissions. Scopes: what a token may do (`salary:read`). Ownership/attribute rules: "my own record", "my department's records". Enforce on the server for every request, ideally also at the gateway; hide with 404 when existence is sensitive.
- **Demo (run: agent):** the salary example, same request, three users.
  ```bash
  B=http://localhost:8000
  for who in HR MGR EMP; do
    t=${!who}
    echo "$who -> employee 7 (Engineering): $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $t" $B/v2/employees/7)   employee 1 (HR head): $(curl -s -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $t" $B/v2/employees/1)"
  done
  curl -s -H "Authorization: Bearer $EMP" $B/v2/auth/me
  curl -si -H "Authorization: Bearer $MGR" "$B/v2/employees?limit=100" | grep -i x-total-count
  ```
  **Point out (verified):** all three get `200` for employee 7; for employee 1 (HR head) only hr_admin gets `200`, the manager and the employee get `403`. `/v2/auth/me` shows the identity the server read from the token. The manager's list is scoped to their department (`x-total-count: 7`). A list as hr_admin returns everyone. Writes (POST/PUT/PATCH/DELETE) are hr_admin-only: try `DELETE /v2/employees/20` with `$MGR` for a `403`.
- **Ask:**
  - Q: Where should the "can this user see salary?" check live? — A: On the server, per request; hiding a field in the UI is not security.
  - Q: RBAC vs ownership rules? — A: Roles decide what kind of thing you can do; ownership decides which records.
- **Done when:** they can predict the response for a new user/record pair.

### Beat 4.8 — The HR token flow end to end
- **Slides:** 67–69 (rewritten for employees)
- **Say:** log in with credentials → receive an access token → send it as a bearer on every call → refresh before it expires.
- **Demo (run: instructor):** in Swagger UI (`http://localhost:8000/docs`) click **Authorize**, enter username `hr_admin` and the demo password (instructor reads it privately with `docker compose exec -T api printenv DEMO_PASSWORD`), then try `GET /v2/employees/7`. Or in Postman use folder **6 Auth (Module 4)**, which saves each token to a variable.
- **Ask:**
  - Q: Where does the client put the token on each request? — A: The `Authorization: Bearer` header.
- **Done when:** every candidate has made one authenticated call.

---

## Exercise (candidates, ~25 min)
Log in as each role and fetch employee 2 and employee 7: record status and whether `salary` appears. Then decode one token and list its claims. Stretch: add a `payroll` role that can read salary but not edit employees.

## Done-check
1. 401 vs 403 in three scenarios.
2. Decode a Basic header and a JWT payload.
3. Explain why signed is not encrypted.
4. Explain expiry, refresh and revocation.
5. Predict who sees salary in the HR example.

## Clean-up
`scripts/setup.sh --reset`; unset the `$HR $MGR $EMP $TOKEN` shell variables.
