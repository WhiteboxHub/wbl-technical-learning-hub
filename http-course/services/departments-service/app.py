"""departments-service (Module 7): owns department data in its own database."""
import json
import logging
import os
import sqlite3
import uuid

from fastapi import FastAPI, HTTPException, Request

NAME = "departments-service"
logging.basicConfig(level=logging.INFO, format="%(message)s")
log = logging.getLogger(NAME)

db = sqlite3.connect(os.getenv("DB_PATH", "/tmp/departments.db"), check_same_thread=False)
db.row_factory = sqlite3.Row
db.execute("CREATE TABLE IF NOT EXISTS departments (id INTEGER PRIMARY KEY, name TEXT, location TEXT)")
if db.execute("SELECT COUNT(*) FROM departments").fetchone()[0] == 0:
    for d in json.load(open("seed_data.json"))["departments"]:
        db.execute("INSERT INTO departments VALUES (?,?,?)", (d["id"], d["name"], d["location"]))
    db.commit()

app = FastAPI(title=NAME)


@app.middleware("http")
async def request_id_and_log(request: Request, call_next):
    rid = request.headers.get("x-request-id") or uuid.uuid4().hex
    response = await call_next(request)
    response.headers["X-Request-Id"] = rid
    response.headers["X-Served-By"] = NAME
    log.info("[%s] rid=%s %s %s -> %s", NAME, rid, request.method, request.url.path, response.status_code)
    return response


@app.get("/health")
def health():
    return {"status": "ok", "service": NAME}


@app.get("/v2/departments")
def list_departments():
    return [dict(r) for r in db.execute("SELECT * FROM departments ORDER BY id")]


@app.get("/v2/departments/{dept_id}")
def get_department(dept_id: int):
    row = db.execute("SELECT * FROM departments WHERE id=?", (dept_id,)).fetchone()
    if row is None:
        raise HTTPException(404, f"department {dept_id} not found")
    return dict(row)
