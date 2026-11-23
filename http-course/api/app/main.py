import json
import os
import secrets
from contextlib import asynccontextmanager

from fastapi import APIRouter, Depends, FastAPI, Header, HTTPException, Query, Request, Response
from fastapi.encoders import jsonable_encoder
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from . import auth, extras, models, schemas
from .database import Base, SessionLocal, engine, get_db
from .seed import seed_if_empty


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(engine)
    with SessionLocal() as db:
        seed_if_empty(db)
    yield


_redis_client = None


def _redis():
    """Optional Redis (cache-aside for the departments list, Module 6). None if unavailable."""
    global _redis_client
    url = os.getenv("REDIS_URL")
    if not url:
        return None
    if _redis_client is None:
        import redis
        _redis_client = redis.Redis.from_url(url, socket_connect_timeout=0.3, socket_timeout=0.3, decode_responses=True)
    return _redis_client


DEPT_CACHE_KEY = "departments:list"
DEPT_CACHE_TTL = 30


def _invalidate_departments():
    try:
        r = _redis()
        if r:
            r.delete(DEPT_CACHE_KEY)
    except Exception:
        pass


app = FastAPI(title="HR API", version="2", lifespan=lifespan)
router = APIRouter(prefix="/v2", dependencies=[Depends(auth.authenticate)])  # every /v2 route needs auth when AUTH=1
extras.install_problem_json(app)  # RFC 7807 errors when PROBLEM_JSON=1 (Module 3)

# CORS is off unless CORS_ORIGINS is set (comma-separated origins). Module 2 turns it on
# with docker-compose.cors.yml so candidates see the browser error first, then the fix.
_cors_origins = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]
if _cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["X-Total-Count", "ETag", "Location"],
    )


def _get_or_404(db: Session, model, obj_id: int, label: str):
    obj = db.get(model, obj_id)
    if obj is None:
        raise HTTPException(status_code=404, detail=f"{label} {obj_id} not found")
    return obj


def _check_refs(db: Session, department_id: int | None, manager_id: int | None):
    if department_id is not None and db.get(models.Department, department_id) is None:
        raise HTTPException(status_code=422, detail=f"department_id {department_id} does not exist")
    if manager_id is not None and db.get(models.Employee, manager_id) is None:
        raise HTTPException(status_code=422, detail=f"manager_id {manager_id} does not exist")


def _save(db: Session):
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="conflict: duplicate value or referenced record")


@app.get("/health")
def health():
    return {"status": "ok"}


# ---- cookie demo (Module 2) ------------------------------------------------

@app.get("/demo/cookie")
def demo_cookie(response: Response):
    """Sets two cookies with different attributes so candidates can compare them."""
    response.set_cookie("session_id", secrets.token_hex(8), httponly=True, samesite="lax", path="/")
    response.set_cookie("theme", "dark", max_age=3600, samesite="lax", path="/")
    return {"message": "cookies set: session_id (HttpOnly) and theme (readable by JS)"}


@app.get("/demo/basic")
def demo_basic(p: auth.Principal = Depends(auth.basic_demo)):
    """Protected with HTTP Basic (Module 4)."""
    return {"authenticated_as": p.username, "role": p.role}


@app.get("/demo/whoami")
def demo_whoami(request: Request):
    """Echoes the cookies the browser or client sent back."""
    return {"cookies_received": dict(request.cookies)}


# ---- departments ----------------------------------------------------------

@router.get("/departments", response_model=list[schemas.DepartmentOut])
def list_departments(response: Response, db: Session = Depends(get_db)):
    """Cache-aside with Redis: header X-Cache-Status says HIT, MISS or BYPASS (no Redis)."""
    try:
        r = _redis()
        cached = r.get(DEPT_CACHE_KEY) if r else None
    except Exception:
        r, cached = None, None
    if cached:
        response.headers["X-Cache-Status"] = "HIT"
        return json.loads(cached)
    rows = db.scalars(select(models.Department).order_by(models.Department.id)).all()
    if r is None:
        response.headers["X-Cache-Status"] = "BYPASS"
        return rows
    data = jsonable_encoder([schemas.DepartmentOut.model_validate(d) for d in rows])
    try:
        r.setex(DEPT_CACHE_KEY, DEPT_CACHE_TTL, json.dumps(data))
    except Exception:
        pass
    response.headers["X-Cache-Status"] = "MISS"
    return data


@router.post("/departments", response_model=schemas.DepartmentOut, status_code=201)
def create_department(body: schemas.DepartmentIn, response: Response, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    dept = models.Department(**body.model_dump())
    db.add(dept)
    _save(db)
    _invalidate_departments()
    db.refresh(dept)
    response.headers["Location"] = f"/v2/departments/{dept.id}"
    return dept


@router.get("/departments/{dept_id}", response_model=schemas.DepartmentOut)
def get_department(dept_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, models.Department, dept_id, "department")


@router.put("/departments/{dept_id}", response_model=schemas.DepartmentOut)
def replace_department(dept_id: int, body: schemas.DepartmentIn, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    dept = _get_or_404(db, models.Department, dept_id, "department")
    for key, value in body.model_dump().items():
        setattr(dept, key, value)
    _save(db)
    _invalidate_departments()
    db.refresh(dept)
    return dept


@router.delete("/departments/{dept_id}", status_code=204)
def delete_department(dept_id: int, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    dept = _get_or_404(db, models.Department, dept_id, "department")
    db.delete(dept)
    _save(db)
    _invalidate_departments()
    return Response(status_code=204)


@router.get("/departments/{dept_id}/employees", response_model=list[schemas.EmployeeOut])
def department_employees(dept_id: int, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    _get_or_404(db, models.Department, dept_id, "department")
    auth.forbid_unless(p.role == "hr_admin" or (p.role == "manager" and p.dept == dept_id))
    stmt = select(models.Employee).where(models.Employee.department_id == dept_id).order_by(models.Employee.id)
    return db.scalars(stmt).all()


# ---- employees ------------------------------------------------------------

SORTABLE = {"id", "name", "title", "hire_date", "salary", "department_id"}


@router.get("/employees", response_model=list[schemas.EmployeeOut])
def list_employees(
    response: Response,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    department_id: int | None = None,
    q: str | None = Query(None, min_length=1, description="case-insensitive search in name, email, title"),
    sort: str = Query("id", description="field name; prefix with - for descending, e.g. -hire_date"),
    p: auth.Principal = Depends(auth.authenticate),
    db: Session = Depends(get_db),
):
    field = sort.lstrip("-")
    if field not in SORTABLE:
        raise HTTPException(status_code=422, detail=f"cannot sort by '{field}'; allowed: {sorted(SORTABLE)}")
    col = getattr(models.Employee, field)
    filters = []
    if p.role == "manager":      # managers only see their own department
        filters.append(models.Employee.department_id == p.dept)
    elif p.role == "employee":   # employees only see themselves
        filters.append(models.Employee.id == p.emp)
    if department_id is not None:
        filters.append(models.Employee.department_id == department_id)
    if q:
        like = f"%{q.lower()}%"
        filters.append(or_(func.lower(models.Employee.name).like(like),
                           func.lower(models.Employee.email).like(like),
                           func.lower(models.Employee.title).like(like)))
    total = db.scalar(select(func.count()).select_from(models.Employee).where(*filters))
    stmt = select(models.Employee).where(*filters).order_by(col.desc() if sort.startswith("-") else col, models.Employee.id).limit(limit).offset(offset)
    response.headers["X-Total-Count"] = str(total)
    return db.scalars(stmt).all()


@router.post("/employees", response_model=schemas.EmployeeOut, status_code=201)
def create_employee(
    body: schemas.EmployeeIn,
    response: Response,
    idempotency_key: str | None = Header(None, description="repeat the same key to safely retry a create"),
    p: auth.Principal = Depends(auth.authenticate),
    db: Session = Depends(get_db),
):
    auth.require_admin(p)
    fingerprint = extras.body_fingerprint(body)
    replay = extras.idempotent_replay(idempotency_key, fingerprint)
    if replay is not None:
        return replay
    _check_refs(db, body.department_id, body.manager_id)
    emp = models.Employee(**body.model_dump())
    db.add(emp)
    _save(db)
    db.refresh(emp)
    location = f"/v2/employees/{emp.id}"
    response.headers["Location"] = location
    out = schemas.EmployeeOut.model_validate(emp)
    extras.remember(idempotency_key, fingerprint, jsonable_encoder(out), location)
    return out


@router.get("/employees/{emp_id}", response_model=schemas.EmployeeOut)
def get_employee(emp_id: int, request: Request, response: Response, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    emp = _get_or_404(db, models.Employee, emp_id, "employee")
    auth.forbid_unless(auth.can_read_employee(p, emp))
    etag = extras.employee_etag(emp)
    if request.headers.get("if-none-match") == etag:
        return Response(status_code=304, headers={"ETag": etag})
    response.headers["ETag"] = etag
    return emp


@router.put("/employees/{emp_id}", response_model=schemas.EmployeeOut)
def replace_employee(emp_id: int, body: schemas.EmployeeIn, request: Request, response: Response, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    emp = _get_or_404(db, models.Employee, emp_id, "employee")
    extras.check_if_match(request, extras.employee_etag(emp))
    _check_refs(db, body.department_id, body.manager_id)
    for key, value in body.model_dump().items():
        setattr(emp, key, value)
    _save(db)
    db.refresh(emp)
    response.headers["ETag"] = extras.employee_etag(emp)
    return emp


@router.patch("/employees/{emp_id}", response_model=schemas.EmployeeOut)
def update_employee(emp_id: int, body: schemas.EmployeePatch, request: Request, response: Response, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    emp = _get_or_404(db, models.Employee, emp_id, "employee")
    extras.check_if_match(request, extras.employee_etag(emp))
    changes = body.model_dump(exclude_unset=True)
    _check_refs(db, changes.get("department_id"), changes.get("manager_id"))
    for key, value in changes.items():
        setattr(emp, key, value)
    _save(db)
    db.refresh(emp)
    response.headers["ETag"] = extras.employee_etag(emp)
    return emp


@router.delete("/employees/{emp_id}", status_code=204)
def delete_employee(emp_id: int, p: auth.Principal = Depends(auth.authenticate), db: Session = Depends(get_db)):
    auth.require_admin(p)
    emp = _get_or_404(db, models.Employee, emp_id, "employee")
    db.delete(emp)
    _save(db)
    return Response(status_code=204)


app.include_router(auth.router)
app.include_router(router)
