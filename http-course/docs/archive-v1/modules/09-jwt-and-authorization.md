# Module 9 — JWT and Authorization (detailed TOC, draft v1)

All new. Slides 68–69 ("OAuth2 token", "External token or assertion") are image-only and may hold a start.

## 9.1 Sessions vs tokens
- Server-side session (cookie + store) vs stateless token
- Scaling, revocation, mobile and API clients
- Decision table

## 9.2 JWT anatomy
- Header, payload, signature; Base64URL
- Registered claims: `iss`, `sub`, `aud`, `exp`, `iat`, `nbf`, `jti`
- Custom claims: `role`, `department_id`
- Decoding a JWT by hand and at jwt.io
- Signed is not encrypted: never put secrets in the payload

## 9.3 Signing algorithms
- HS256 (shared secret) vs RS256/ES256 (public/private key)
- JWKS endpoint and key rotation (overview)
- `alg: none` and algorithm-confusion attacks

## 9.4 Token lifecycle
- Access token (short-lived) + refresh token (long-lived)
- Refresh flow, rotation, reuse detection
- Revocation: blocklists, short expiry, token versioning
- Logout reality for stateless tokens

## 9.5 Validating a token
- Check signature, `exp`, `iss`, `aud`, `nbf`
- FastAPI dependency that validates and extracts the user

## 9.6 Authorization models
- RBAC: roles (`hr_admin`, `manager`, `employee`)
- Scopes (`employees:read`, `salary:read`)
- ABAC/ownership: "manager of this department", "my own record"
- Where to enforce: gateway vs service

## 9.7 HR salary example
- `GET /employees/5` as HR admin → full record with salary
- As manager of that department → salary visible; other manager → 403
- As employee 5 → own record with salary; other employee → 403 or redacted
- Field-level filtering in the response model

## 9.8 Authorization failures
- 401 vs 403 vs 404 (hiding existence)
- Audit logging of access to sensitive data

## 9.9 Common mistakes
- Long-lived access tokens, secrets in payload, trusting unsigned tokens, storing in localStorage (see 3.8, 11.1)

## Labs
1. Decode a token from the HR API and name every claim
2. Tamper with the payload and watch validation fail
3. Let a token expire, use the refresh flow
4. Prove three roles see three different views of `/employees/5`
5. Candidate exercise: add a `payroll` role that can read salary but not edit employees

## Candidate question bank (sample)
- What are the three parts of a JWT?
- Why can anyone read a JWT payload?
- Why short-lived access tokens?
- RBAC vs scopes?

## Slide work
- **Add:** about 12 slides (new module)
