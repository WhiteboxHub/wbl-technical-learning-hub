"""INTENTIONALLY VULNERABLE demo app for Module 5. Never deploy this.

Each weakness has a fixed variant behind ?fixed=1 so candidates can compare:
  /notes            stored XSS       fixed: output is HTML-escaped
  POST /delete      CSRF             fixed: Origin check + per-session token
  /search?q=        SQL injection    fixed: parameterized query
"""
import html
import secrets
import sqlite3

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, JSONResponse

app = FastAPI(title="vuln (do not deploy)")

db = sqlite3.connect(":memory:", check_same_thread=False)
db.execute("CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, title TEXT, salary REAL)")
db.executemany("INSERT INTO employees (name, title, salary) VALUES (?,?,?)", [
    ("Priya Raman", "Head of HR", 185000), ("Marcus Lee", "Engineering Director", 210000),
    ("Elena Garcia", "Finance Director", 195000), ("Sofia Rossi", "Senior Engineer", 165000),
    ("Ravi Patel", "Engineer", 135000), ("Mei Chen", "Account Executive", 92000)])
db.commit()

NOTES: list[str] = []
CSRF_TOKEN = secrets.token_hex(8)   # one demo session
ORIGIN = "http://localhost:3003"


def page(body: str, fixed: bool) -> HTMLResponse:
    mode = "FIXED" if fixed else "VULNERABLE"
    return HTMLResponse(f"""<!doctype html><meta charset=utf-8><title>vuln demo</title>
<body style="font:16px system-ui;max-width:760px;margin:24px auto;padding:0 16px">
<h1>Module 5 demo app <small>[{mode}]</small></h1>
<p><a href="/">home</a> | <a href="/notes{'?fixed=1' if fixed else ''}">notes (XSS)</a> |
<a href="/search{'?fixed=1' if fixed else ''}">search (SQLi)</a> | <a href="/employees{'?fixed=1' if fixed else ''}">employees (CSRF)</a> |
<a href="{'/?' if fixed else '/?fixed=1'}">{'switch to VULNERABLE' if fixed else 'switch to FIXED'}</a></p>{body}""")


def is_fixed(request: Request) -> bool:
    return request.query_params.get("fixed") == "1"


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    resp = page("<p>Three weaknesses to find, exploit and fix. Log in first: it sets a session cookie.</p>"
                "<form method=post action='/login'><button>Log in as hr_admin</button></form>", is_fixed(request))
    return resp


@app.post("/login")
def login():
    resp = HTMLResponse("<meta http-equiv=refresh content='0;url=/employees'>logged in")
    resp.set_cookie("session", "hr_admin", httponly=True, path="/")  # no CSRF protection, no SameSite set
    return resp


# ---- 1. stored XSS ---------------------------------------------------------
@app.get("/notes", response_class=HTMLResponse)
def notes(request: Request):
    fixed = is_fixed(request)
    items = "".join(f"<li>{html.escape(n) if fixed else n}</li>" for n in NOTES) or "<li><i>no notes yet</i></li>"
    q = "?fixed=1" if fixed else ""
    return page(f"<h2>Team notes</h2><form method=post action='/notes{q}'><input name=text size=50 placeholder='write a note'>"
                f"<button>Add</button></form><ul>{items}</ul>", fixed)


@app.post("/notes")
def add_note(request: Request, text: str = Form(...)):
    NOTES.append(text)
    return HTMLResponse(f"<meta http-equiv=refresh content='0;url=/notes{'?fixed=1' if is_fixed(request) else ''}'>saved")


# ---- 2. CSRF ---------------------------------------------------------------
@app.get("/employees", response_class=HTMLResponse)
def employees(request: Request):
    fixed = is_fixed(request)
    rows = db.execute("SELECT id, name, title FROM employees ORDER BY id").fetchall()
    token = f"<input type=hidden name=csrf value='{CSRF_TOKEN}'>" if fixed else ""
    q = "?fixed=1" if fixed else ""
    body = "".join(f"<tr><td>{i}</td><td>{html.escape(n)}</td><td>{html.escape(t)}</td>"
                   f"<td><form method=post action='/delete{q}'><input type=hidden name=id value={i}>{token}<button>delete</button></form></td></tr>"
                   for i, n, t in rows)
    return page(f"<h2>Employees</h2><table border=1 cellpadding=6><tr><th>id</th><th>name</th><th>title</th><th></th></tr>{body}</table>"
                "<p>Evil page that deletes employee 4 using your cookie: <a href='http://localhost:3000/evil.html' target=_blank>open evil.html</a></p>", fixed)


@app.post("/delete")
def delete(request: Request, id: int = Form(...), csrf: str = Form("")):
    if request.cookies.get("session") != "hr_admin":
        return JSONResponse({"detail": "not logged in"}, status_code=401)
    if is_fixed(request):
        origin = request.headers.get("origin")
        if origin != ORIGIN or csrf != CSRF_TOKEN:
            return JSONResponse({"detail": "blocked: bad Origin or missing CSRF token"}, status_code=403)
    db.execute("DELETE FROM employees WHERE id=?", (id,))
    db.commit()
    return HTMLResponse(f"<meta http-equiv=refresh content='0;url={ORIGIN}/employees{'?fixed=1' if is_fixed(request) else ''}'>deleted {id}")


# ---- 3. SQL injection -------------------------------------------------------
@app.get("/search", response_class=HTMLResponse)
def search(request: Request, q: str = ""):
    fixed = is_fixed(request)
    form = f"<form><input name=q value='{html.escape(q)}' size=40>{'<input type=hidden name=fixed value=1>' if fixed else ''}<button>Find by exact name</button></form>"
    result = ""
    if q:
        try:
            if fixed:
                rows = db.execute("SELECT name, title, salary FROM employees WHERE name = ?", (q,)).fetchall()
            else:
                rows = db.execute(f"SELECT name, title, salary FROM employees WHERE name = '{q}'").fetchall()  # noqa: S608 (the bug)
            result = "<table border=1 cellpadding=6>" + "".join(
                f"<tr><td>{html.escape(n)}</td><td>{html.escape(t)}</td><td>{s}</td></tr>" for n, t, s in rows) + "</table>" if rows else "<p>no match</p>"
        except sqlite3.Error as e:
            result = f"<p>SQL error: {html.escape(str(e))}</p>"
    return page(f"<h2>Search (shows salary)</h2>{form}{result}", fixed)


@app.get("/health")
def health():
    return {"status": "ok"}
