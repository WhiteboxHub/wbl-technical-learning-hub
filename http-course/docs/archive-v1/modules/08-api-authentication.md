# Module 8 — API Authentication: Basic, API Key, OAuth 2.0 (detailed TOC, draft v1)

Status: **Have** · **Thin** · **Add**. Slides 61–69. Slides 67–69 use the students API, convert to HR.

## 8.1 Authentication vs authorization
- Who are you vs what may you do
- Identification, authentication, authorization, accounting
- 401 vs 403
Slide 62 · **Have** (add 401/403 pairing)

## 8.2 Basic authentication
- `Authorization: Basic base64(user:pass)`; Base64 is not encryption
- Needs HTTPS; no logout; credentials sent every request
Slide 61 · **Have**

## 8.3 API keys
- Identification, not true authentication
- Header vs query param (never in URL), rotation, scoping
- Use cases: server-to-server, public data with quotas
Slide 64 · **Have**

## 8.4 Bearer tokens
- `Authorization: Bearer <token>`
- Opaque vs self-contained tokens (JWT in Module 9)
- Expiry, revocation
**Add**

## 8.5 OAuth 1.0 vs 2.0
- Why OAuth exists: delegated access without sharing passwords
- 1.0 signatures vs 2.0 bearer tokens
Slides 65, 66 · **Have**

## 8.6 OAuth 2.0 concepts
- Roles: resource owner, client, authorization server, resource server
- Access token, refresh token, scope, client ID/secret, redirect URI
- Grant types overview (detail in Module 10)
Slide 66 · **Thin** (roles diagram)

## 8.7 The HR API token flow
- Get access token: `GET /v2/employees/auth/` with `x-auth-token`
- Call protected endpoint with the token
Slides 67, 68, 69 · **Have** (rename to employees; replace `x-auth-token` demo with a proper `POST /token`)

## 8.8 Password handling basics
- Hashing vs encryption, bcrypt/argon2, salt
- Never store plaintext; never log secrets
**Add**

## 8.9 Choosing a method
| Method | Use for | Weakness |
|---|---|---|
| Basic | internal, quick | credentials every call |
| API key | server-to-server | no user identity |
| Bearer/OAuth2 | user-delegated access | complexity |

## Labs
1. Call the HR API with no auth (401), wrong auth (401), wrong role (403)
2. Basic auth with `curl -u`, decode the header by hand
3. Obtain and use a bearer token in Postman
4. Candidate exercise: protect `DELETE /employees/{id}`

## Candidate question bank (sample)
- Authentication vs authorization?
- Why is Base64 not security?
- What problem does OAuth solve?

## Slide work
- **Fix:** 67–69 to HR; add 401/403
- **Add:** bearer tokens, password hashing (about 3 slides)
