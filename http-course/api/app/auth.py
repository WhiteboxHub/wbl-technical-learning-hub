"""Module 4: authentication and authorization (JWT bearer, HTTP Basic demo, roles).

Off by default so Modules 1-3 keep working. Turn on with AUTH=1 (docker-compose.auth.yml).
All credentials here are dev-only demo values read from the environment.
"""
import hashlib
import hmac
import os
import secrets
import time
from dataclasses import dataclass
from functools import lru_cache

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

ISSUER = "hr-api"
AUDIENCE = "hr-clients"
ALGORITHM = "HS256"


@dataclass
class Principal:
    username: str
    role: str          # hr_admin | manager | employee
    dept: int | None   # department the user manages or belongs to
    emp: int | None    # their own employee record


# username -> (role, employee id, department id). Matches the seed data.
USERS = {
    "hr_admin": ("hr_admin", 1, 1),   # Priya Raman, Head of HR
    "manager": ("manager", 2, 2),     # Marcus Lee, Engineering Director
    "employee": ("employee", 7, 2),   # Sofia Rossi, Senior Engineer
}


def auth_mode() -> str:
    """off | local (our own JWTs) | oidc (tokens issued by Keycloak)."""
    v = os.getenv("AUTH", "0").lower()
    return "oidc" if v == "oidc" else ("local" if v in ("1", "true", "yes", "local") else "off")


def auth_enabled() -> bool:
    return auth_mode() != "off"


def token_ttl() -> int:
    return int(os.getenv("TOKEN_TTL", "900"))


def _secret() -> str:
    return os.getenv("JWT_SECRET", "dev-only-secret-not-for-production-use-0123456789")


# ---- passwords: stored as salted PBKDF2 hashes, compared in constant time ----

def _hash(password: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 200_000)


@lru_cache
def _credentials(demo_password: str) -> dict[str, tuple[bytes, bytes]]:
    out = {}
    for username in USERS:
        salt = secrets.token_bytes(16)
        out[username] = (salt, _hash(demo_password, salt))
    return out


def verify_login(username: str, password: str) -> Principal | None:
    demo_password = os.getenv("DEMO_PASSWORD")
    if not demo_password:
        raise HTTPException(status_code=503, detail="DEMO_PASSWORD is not configured on the server")
    creds = _credentials(demo_password)
    if username not in creds:
        return None
    salt, expected = creds[username]
    if not hmac.compare_digest(_hash(password, salt), expected):
        return None
    role, emp, dept = USERS[username]
    return Principal(username, role, dept, emp)


# ---- tokens ------------------------------------------------------------------

def create_token(p: Principal) -> str:
    now = int(time.time())
    payload = {"iss": ISSUER, "aud": AUDIENCE, "sub": p.username, "role": p.role,
               "dept": p.dept, "emp": p.emp, "iat": now, "exp": now + token_ttl()}
    return jwt.encode(payload, _secret(), algorithm=ALGORITHM)


def _unauthorized(detail: str) -> HTTPException:
    return HTTPException(status_code=401, detail=detail, headers={"WWW-Authenticate": "Bearer"})


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v2/auth/token", auto_error=False)  # enables Swagger's Authorize button


def authenticate(token: str | None = Depends(oauth2_scheme)) -> Principal:
    if not auth_enabled():
        return Principal("anonymous", "hr_admin", None, None)  # auth off: everything allowed
    if not token:
        raise _unauthorized("missing bearer token")
    if auth_mode() == "oidc":
        return _authenticate_oidc(token)
    try:
        claims = jwt.decode(token, _secret(), algorithms=[ALGORITHM], audience=AUDIENCE, issuer=ISSUER)
    except jwt.ExpiredSignatureError:
        raise _unauthorized("token expired")
    except jwt.PyJWTError:
        raise _unauthorized("invalid token")
    return Principal(claims["sub"], claims["role"], claims.get("dept"), claims.get("emp"))


_jwks_client = None


def _authenticate_oidc(token: str) -> Principal:
    """Validate a Keycloak token: signature via the realm's public keys (JWKS), expiry and issuer.
    Audience is not checked in this demo. The user's role comes from the IdP's realm roles; the
    employee/department ids come from our own USERS table, keyed by the IdP username."""
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = jwt.PyJWKClient(os.getenv("OIDC_JWKS_URL", "http://keycloak:8080/realms/hr/protocol/openid-connect/certs"))
    try:
        key = _jwks_client.get_signing_key_from_jwt(token).key
        claims = jwt.decode(token, key, algorithms=["RS256"], issuer=os.getenv("OIDC_ISSUER", "http://localhost:8081/realms/hr"),
                            options={"verify_aud": False})
    except jwt.ExpiredSignatureError:
        raise _unauthorized("token expired")
    except Exception:
        raise _unauthorized("invalid token")
    username = claims.get("preferred_username", "")
    roles = [r for r in claims.get("realm_access", {}).get("roles", []) if r in ("hr_admin", "manager", "employee")]
    if username not in USERS or not roles:
        raise HTTPException(status_code=403, detail="no HR role for this identity")
    _, emp, dept = USERS[username]
    return Principal(username, roles[0], dept, emp)


# ---- authorization rules -------------------------------------------------------

def require_admin(p: Principal) -> None:
    if p.role != "hr_admin":
        raise HTTPException(status_code=403, detail="hr_admin role required")


def can_read_employee(p: Principal, emp) -> bool:
    return (p.role == "hr_admin"
            or (p.role == "manager" and emp.department_id == p.dept)
            or (p.role == "employee" and emp.id == p.emp))


def forbid_unless(allowed: bool, detail: str = "you are not allowed to see this record") -> None:
    if not allowed:
        raise HTTPException(status_code=403, detail=detail)


# ---- routes ---------------------------------------------------------------------

router = APIRouter(prefix="/v2/auth", tags=["auth"])


@router.post("/token")
def login(form: OAuth2PasswordRequestForm = Depends()):
    principal = verify_login(form.username, form.password)
    if principal is None:
        raise HTTPException(status_code=401, detail="incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    return {"access_token": create_token(principal), "token_type": "bearer", "expires_in": token_ttl()}


@router.get("/me")
def me(p: Principal = Depends(authenticate)):
    return {"username": p.username, "role": p.role, "dept": p.dept, "emp": p.emp}


basic = HTTPBasic(auto_error=False)


def basic_demo(credentials: HTTPBasicCredentials | None = Depends(basic)):
    """HTTP Basic: the browser/curl sends base64(user:password) on every request."""
    if credentials is None:
        raise HTTPException(status_code=401, detail="Basic credentials required", headers={"WWW-Authenticate": 'Basic realm="hr-demo"'})
    p = verify_login(credentials.username, credentials.password)
    if p is None:
        raise HTTPException(status_code=401, detail="incorrect username or password", headers={"WWW-Authenticate": 'Basic realm="hr-demo"'})
    return p
