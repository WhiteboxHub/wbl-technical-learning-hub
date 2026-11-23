"""employees-service (Module 7): owns employee data in its own database.

Calls departments-service over HTTP with a 1 s timeout and a circuit breaker, and
publishes an EmployeeHired event to a Redis stream when an employee is created.
"""
import json
import logging
import os
import sqlite3
import time
import uuid

import httpx
import redis
from fastapi import FastAPI, HTTPException, Query, Request, Response
from pydantic import BaseModel

NAME = "employees-service"
DEPARTMENTS_URL = os.getenv("DEPARTMENTS_URL", "http://departments-service:8000")
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(NAME)

db = sqlite3.connect(os.getenv("DB_PATH", "/tmp/employees.db"), check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("""CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE,
              title TEXT, department_id INTEGER, manager_id INTEGER, hire_date TEXT, salary REAL)""")
if db.execute("SELECT COUNT(*) FROM employees").fetchone()[0] == 0:
    for e in json.load(open("seed_data.json"))["employees"]:
        db.execute("INSERT INTO employees VALUES (:id,:name,:email,:title,:department_id,:manager_id,:hire_date,:salary)", e)
    db.commit()

app = FastAPI(title=NAME)
events = redis.Redis.from_url(os.getenv("REDIS_URL", "redis://redis:6379/0"), socket_connect_timeout=0.5, socket_timeout=0.5, decode_responses=True)


class CircuitBreaker:
    """closed -> (3 failures) -> open (fail fast for 10 s) -> half-open (one probe) -> closed."""

    def __init__(self, threshold=3, reset_after=10.0):
        self.threshold, self.reset_after = threshold, reset_after
        self.failures, self.opened_at = 0, None

    @property
    def state(self):
        if self.opened_at is None:
            return "closed"
        return "half-open" if time.time() - self.opened_at >= self.reset_after else "open"

    def allow(self):
        return self.state != "open"

    def success(self):
        self.failures, self.opened_at = 0, None

    def failure(self):
        self.failures += 1
        if self.failures >= self.threshold or self.state == "half-open":
            self.opened_at = time.time()


breaker = CircuitBreaker()


class EmployeeIn(BaseModel):
    name: str
    email: str
    title: str
    department_id: int
    manager_id: int | None = None
    hire_date: str
    salary: float


@app.middleware("http")
async def request_id_and_log(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    request.state.rid = rid
    response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    response.headers["X-Served-By"] = NAME
    log.info("[%s] rid=%s %s %s -> %s", NAME, rid, request.method, request.url.path, response.status_code)
    return response


@app.get("/health")
def health():
    return {"status": "ok", "service": NAME, "breaker": breaker.state}


@app.get("/v2/employees")
def list_employees(response: Response, limit: int = Query(20, ge=1, le=100), offset: int = Query(0, ge=0)):
    total = db.execute("SELECT COUNT(*) FROM employees").fetchone()[0]
    response.headers["X-Total-Count"] = str(total)
    return [dict(r) for r in db.execute("SELECT * FROM employees ORDER BY id LIMIT ? OFFSET ?", (limit, offset))]


@app.get("/v2/employees/{emp_id}")
def get_employee(emp_id: int, request: Request, response: Response, expand: str | None = None):
    row = db.execute("SELECT * FROM employees WHERE id=?", (emp_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"employee {emp_id} not found")
    emp = dict(row)
    if expand == "department":
        emp["department"] = fetch_department(emp["department_id"], request.state.rid, response)
    return emp


def fetch_department(dept_id: int, rid: str, response: Response):
    """Call the other service: timeout + circuit breaker + fallback."""
    fallback = {"id": dept_id, "name": None, "degraded": True}
    if not breaker.allow():
        response.headers["X-Breaker"] = "open"
        return {**fallback, "note": "departments-service unavailable (circuit open, failing fast)"}
    try:
        r = httpx.get(f"{DEPARTMENTS_URL}/v2/departments/{dept_id}", headers={"X-Request-Id": rid}, timeout=1.0)
        r.raise_for_status()
        breaker.success()
        response.headers["X-Breaker"] = "closed"
        return r.json()
    except Exception as exc:  # timeout, refused, 5xx: all count as a failure
        breaker.failure()
        response.headers["X-Breaker"] = breaker.state
        log.warning("[%s] rid=%s departments-service call failed (%s); breaker=%s", NAME, rid, type(exc).__name__, breaker.state)
        return {**fallback, "note": f"departments-service call failed ({type(exc).__name__}); breaker {breaker.state}"}


@app.post("/v2/employees", status_code=201)
def create_employee(body: EmployeeIn, request: Request, response: Response):
    try:
        cur = db.execute("INSERT INTO employees (name,email,title,department_id,manager_id,hire_date,salary) VALUES (?,?,?,?,?,?,?)",
                         (body.name, body.email, body.title, body.department_id, body.manager_id, body.hire_date, body.salary))
        db.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(409, "conflict: duplicate email")
    emp_id = cur.lastrowid
    response.headers["Location"] = f"/v2/employees/{emp_id}"
    try:  # publish the event; the employee is already saved, so a Redis outage must not fail the request
        events.xadd("hr.events", {"type": "EmployeeHired", "employee_id": emp_id, "name": body.name,
                                  "department_id": body.department_id, "rid": request.state.rid})
    except Exception as exc:
        log.warning("[%s] rid=%s could not publish event: %s", NAME, request.state.rid, exc)
    return {"id": emp_id, **body.model_dump()}


@app.delete("/v2/employees/{emp_id}", status_code=204)
def delete_employee(emp_id: int):
    db.execute("DELETE FROM employees WHERE id=?", (emp_id,))
    db.commit()
    return Response(status_code=204)
