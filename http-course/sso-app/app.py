"""Tiny OIDC relying party for Module 5. The same code runs as 'portal' (:3001) and 'payroll' (:3002).

Implements authorization code + PKCE by hand so every step is visible in DevTools:
/login -> Keycloak /auth -> /callback?code&state -> back-channel token exchange.
"""
import base64
import hashlib
import html
import json
import os
import secrets
from urllib.parse import urlencode

import httpx
import jwt
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse

CLIENT_ID = os.environ["CLIENT_ID"]
PORT = os.environ["PORT"]
BASE = f"http://localhost:{PORT}"
BROWSER_KC = os.getenv("KC_BROWSER_URL", "http://localhost:8081") + "/realms/hr/protocol/openid-connect"
BACK_KC = os.getenv("KC_BACK_URL", "http://keycloak:8080") + "/realms/hr/protocol/openid-connect"
API = os.getenv("API_URL", "http://api:8000")
COOKIE = f"{CLIENT_ID}_sid"  # cookies are per host, not per port: keep the two apps apart

app = FastAPI(title=f"{CLIENT_ID} (OIDC demo)")
SESSIONS: dict[str, dict] = {}
PENDING: dict[str, str] = {}  # state -> code_verifier


def page(title: str, body: str) -> HTMLResponse:
    return HTMLResponse(f"""<!doctype html><meta charset=utf-8><title>{CLIENT_ID}</title>
<body style="font:16px system-ui;max-width:760px;margin:24px auto;padding:0 16px">
<h1>{html.escape(CLIENT_ID.title())} app <small style="color:#666">:{PORT}</small></h1>{body}
<p style="color:#666">Other app: <a href="http://localhost:{'3002' if PORT == '3001' else '3001'}">open</a></p>""")


def session_of(request: Request):
    return SESSIONS.get(request.cookies.get(COOKIE, ""))


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    s = session_of(request)
    if not s:
        return page("home", "<p>You are not signed in.</p><p><a href='/login'><button>Sign in with SSO</button></a></p>")
    c = s["id_claims"]
    return page("home", f"<p>Signed in as <b>{html.escape(c.get('name', c.get('preferred_username', '?')))}</b> "
                f"(roles: {html.escape(', '.join(s['access_claims'].get('realm_access', {}).get('roles', [])))}).</p>"
                f"<p><a href='/claims'>show tokens' claims</a> | <a href='/api'>call HR API with my token</a></p>"
                f"<p><a href='/logout'>local logout</a> | <a href='/logout-idp'>logout everywhere (IdP)</a></p>")


@app.get("/login")
def login():
    verifier = secrets.token_urlsafe(48)
    state = secrets.token_urlsafe(16)
    PENDING[state] = verifier
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b"=").decode()
    q = urlencode({"client_id": CLIENT_ID, "response_type": "code", "scope": "openid profile email",
                   "redirect_uri": f"{BASE}/callback", "state": state,
                   "code_challenge": challenge, "code_challenge_method": "S256"})
    return RedirectResponse(f"{BROWSER_KC}/auth?{q}")


@app.get("/callback")
def callback(request: Request, code: str = "", state: str = "", error: str = ""):
    if error or state not in PENDING:
        return page("error", f"<p>Login failed: {html.escape(error or 'unknown state (possible CSRF)')}</p>")
    verifier = PENDING.pop(state)
    r = httpx.post(f"{BACK_KC}/token", data={"grant_type": "authorization_code", "client_id": CLIENT_ID, "code": code,
                                             "redirect_uri": f"{BASE}/callback", "code_verifier": verifier})
    if r.status_code != 200:
        return page("error", f"<p>Token exchange failed: {r.status_code} {html.escape(r.text)}</p>")
    tok = r.json()
    sid = secrets.token_urlsafe(24)
    # Claims are read without signature checks here because the token came straight from the IdP over the
    # back channel. The HR API does the real signature check (Module 5, beat 5.6).
    SESSIONS[sid] = {"tokens": tok, "id_claims": jwt.decode(tok["id_token"], options={"verify_signature": False}),
                     "access_claims": jwt.decode(tok["access_token"], options={"verify_signature": False})}
    resp = RedirectResponse("/")
    resp.set_cookie(COOKIE, sid, httponly=True, samesite="lax", path="/")
    return resp


@app.get("/claims", response_class=HTMLResponse)
def claims(request: Request):
    s = session_of(request)
    if not s:
        return RedirectResponse("/")
    return page("claims", f"<h2>ID token claims</h2><pre>{html.escape(json.dumps(s['id_claims'], indent=2))}</pre>"
                          f"<h2>Access token claims</h2><pre>{html.escape(json.dumps(s['access_claims'], indent=2))}</pre><p><a href='/'>back</a></p>")


@app.get("/api", response_class=HTMLResponse)
def call_api(request: Request):
    s = session_of(request)
    if not s:
        return RedirectResponse("/")
    r = httpx.get(f"{API}/v2/employees/7", headers={"Authorization": f"Bearer {s['tokens']['access_token']}"})
    return page("api", f"<h2>GET /v2/employees/7 with my access token</h2><p>Status: <b>{r.status_code}</b></p>"
                       f"<pre>{html.escape(r.text)}</pre><p><a href='/'>back</a></p>")


@app.get("/logout")
def logout(request: Request):
    SESSIONS.pop(request.cookies.get(COOKIE, ""), None)
    resp = RedirectResponse("/")
    resp.delete_cookie(COOKIE, path="/")
    return resp


@app.get("/logout-idp")
def logout_idp(request: Request):
    s = SESSIONS.pop(request.cookies.get(COOKIE, ""), None)
    q = {"client_id": CLIENT_ID, "post_logout_redirect_uri": f"{BASE}/"}
    if s:
        q["id_token_hint"] = s["tokens"]["id_token"]
    resp = RedirectResponse(f"{BROWSER_KC}/logout?{urlencode(q)}")
    resp.delete_cookie(COOKIE, path="/")
    return resp
