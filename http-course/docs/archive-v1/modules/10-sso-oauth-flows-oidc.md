# Module 10 — SSO, OAuth Flows and OIDC (detailed TOC, draft v1)

All new. The biggest gap in the current deck. Demo uses Keycloak in Docker Compose.

## 10.1 The problem SSO solves
- Many apps, many passwords; password fatigue, helpdesk cost, offboarding risk
- HR example: portal, payroll, benefits, timesheets with one login
- Identity provider (IdP) vs service provider/relying party (RP)

## 10.2 Core vocabulary
- Resource owner, client, authorization server, resource server
- Authentication vs authorization (recap of 8.1)
- Access token, ID token, refresh token, scope, claim, redirect URI, client ID/secret

## 10.3 OAuth 2.0 grant types
- **Authorization Code (+ PKCE)**: web and SPA/mobile (recommended)
- **Client Credentials**: service to service
- Device code (awareness)
- Deprecated: implicit, password grant (and why)

## 10.4 Authorization code + PKCE step by step
1. Redirect to IdP with `client_id`, `redirect_uri`, `scope`, `state`, `code_challenge`
2. User logs in and consents
3. Redirect back with `code`
4. Back-channel exchange for tokens with `code_verifier`
5. Call the API with the access token
- `state` and CSRF; why PKCE
- Demo: follow every redirect in DevTools

## 10.5 OpenID Connect (OIDC)
- OAuth is authorization; OIDC adds authentication on top
- ID token (a JWT), `openid` scope, `/userinfo`
- Discovery document `/.well-known/openid-configuration`, JWKS

## 10.6 How SSO works
- Session at the IdP (cookie), silent re-authentication
- Two apps, one login: app A login → app B needs no password prompt
- Cookies across domains, redirects as the mechanism

## 10.7 Logout
- Local logout vs IdP logout vs single logout (RP-initiated, back-channel)
- Why logout is hard

## 10.8 MFA and security features
- Something you know/have/are; TOTP, WebAuthn/passkeys
- Step-up auth for sensitive actions (viewing salaries)

## 10.9 SAML (Stretch)
- XML assertions, enterprise SSO, SAML vs OIDC

## 10.10 Identity providers in the real world
- Keycloak, Okta, Auth0, Azure AD/Entra, Google; build vs buy

## 10.11 Protecting the HR API with OIDC
- API validates IdP-issued JWT using JWKS
- Roles mapped from IdP groups to API roles

## Labs
1. Start Keycloak, create realm, users `hr_admin`, `manager`, `employee`
2. Log in to the HR portal and trace the redirects
3. Open the payroll app: no second login
4. Call the HR API with the access token
5. Log out and prove the second app loses access
6. Candidate exercise: add a third app to the SSO realm

## Candidate question bank (sample)
- OAuth vs OIDC?
- What does PKCE protect against?
- What is in an ID token vs an access token?
- Why is single logout hard?

## Slide work
- **Add:** about 16 slides and 3 sequence diagrams (new module)
