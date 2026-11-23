"""Module 3 teaching helpers: RFC 7807 errors, ETags and idempotency keys."""
import hashlib
import json
import os
from http import HTTPStatus

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from . import schemas


# ---- RFC 7807 problem+json (opt in with PROBLEM_JSON=1) --------------------

def _problem(request: Request, status: int, detail, **extra) -> JSONResponse:
    body = {
        "type": "about:blank",
        "title": HTTPStatus(status).phrase,
        "status": status,
        "detail": detail,
        "instance": request.url.path,
        **extra,
    }
    return JSONResponse(body, status_code=status, media_type="application/problem+json")


def install_problem_json(app: FastAPI) -> None:
    if os.getenv("PROBLEM_JSON", "") not in ("1", "true", "yes"):
        return

    @app.exception_handler(StarletteHTTPException)
    async def _http_exc(request: Request, exc: StarletteHTTPException):
        resp = _problem(request, exc.status_code, exc.detail)
        for k, v in (exc.headers or {}).items():
            resp.headers[k] = v
        return resp

    @app.exception_handler(RequestValidationError)
    async def _validation_exc(request: Request, exc: RequestValidationError):
        errors = [{"field": ".".join(str(p) for p in e["loc"][1:]) or e["loc"][0], "message": e["msg"]} for e in exc.errors()]
        return _problem(request, 422, "Request validation failed", errors=errors)


# ---- ETag / If-Match -------------------------------------------------------

def employee_etag(emp) -> str:
    payload = json.dumps(jsonable_encoder(schemas.EmployeeOut.model_validate(emp)), sort_keys=True)
    return '"' + hashlib.sha1(payload.encode()).hexdigest()[:16] + '"'


def check_if_match(request: Request, current_etag: str) -> None:
    """Optimistic concurrency: if the client sent If-Match and it is stale, refuse with 412."""
    sent = request.headers.get("if-match")
    if sent is not None and sent.strip() != "*" and sent.strip() != current_etag:
        raise HTTPException(status_code=412, detail="The resource changed since you read it (ETag mismatch). Fetch it again and retry.")


# ---- Idempotency-Key (in memory; one API process, demo only) ---------------

_seen: dict[str, tuple[str, dict, str]] = {}


def body_fingerprint(body: schemas.EmployeeIn) -> str:
    return hashlib.sha1(json.dumps(jsonable_encoder(body), sort_keys=True).encode()).hexdigest()


def idempotent_replay(key: str | None, fingerprint: str):
    """Return a replayed response for a repeated key, None if the key is new."""
    if not key or key not in _seen:
        return None
    seen_fp, content, location = _seen[key]
    if seen_fp != fingerprint:
        raise HTTPException(status_code=422, detail="Idempotency-Key was already used with a different request body.")
    return JSONResponse(content, status_code=201, headers={"Location": location, "Idempotent-Replayed": "true"})


def remember(key: str | None, fingerprint: str, content: dict, location: str) -> None:
    if key:
        _seen[key] = (fingerprint, content, location)
