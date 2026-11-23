"""Starter tests for the HR API (Module 3). Run: docker compose run --rm api pytest -q"""
import uuid

from .conftest import new_employee


def unique_email():
    return f"t.{uuid.uuid4().hex[:8]}@example.com"


def test_health(client):
    assert client.get("/health").json() == {"status": "ok"}


def test_seed_data_present(client):
    r = client.get("/v2/employees?limit=100")
    assert r.status_code == 200
    assert len(r.json()) == 20
    assert r.headers["X-Total-Count"] == "20"


def test_get_employee_and_404(client):
    assert client.get("/v2/employees/1").json()["name"] == "Priya Raman"
    assert client.get("/v2/employees/99999").status_code == 404


def test_create_read_update_delete(client):
    email = unique_email()
    created = client.post("/v2/employees", json=new_employee(email=email))
    assert created.status_code == 201
    emp_id = created.json()["id"]
    assert created.headers["Location"] == f"/v2/employees/{emp_id}"

    replaced = client.put(f"/v2/employees/{emp_id}", json=new_employee(email=email, title="Senior Tester"))
    assert replaced.status_code == 200 and replaced.json()["title"] == "Senior Tester"

    patched = client.patch(f"/v2/employees/{emp_id}", json={"salary": 95000})
    assert patched.status_code == 200 and patched.json()["salary"] == 95000

    assert client.delete(f"/v2/employees/{emp_id}").status_code == 204
    assert client.get(f"/v2/employees/{emp_id}").status_code == 404


def test_validation_and_conflicts(client):
    assert client.post("/v2/employees", json={"name": "x"}).status_code == 422
    assert client.post("/v2/employees", json=new_employee(department_id=999, email=unique_email())).status_code == 422
    assert client.post("/v2/employees", json=new_employee(email="priya.raman@example.com")).status_code == 409
    assert client.delete("/v2/departments/2").status_code == 409  # still has employees


def test_pagination_filter_sort_search(client):
    first = client.get("/v2/employees?limit=5&offset=0").json()
    second = client.get("/v2/employees?limit=5&offset=5").json()
    assert not {e["id"] for e in first} & {e["id"] for e in second}
    eng = client.get("/v2/employees?department_id=2&limit=100")
    assert all(e["department_id"] == 2 for e in eng.json())
    assert eng.headers["X-Total-Count"] == str(len(eng.json()))
    by_pay = client.get("/v2/employees?sort=-salary&limit=1").json()[0]
    assert by_pay["name"] == "Marcus Lee"
    assert [e["name"] for e in client.get("/v2/employees?q=garcia").json()] == ["Elena Garcia"]
    assert client.get("/v2/employees?sort=password").status_code == 422


def test_etag_and_conditional_requests(client):
    first = client.get("/v2/employees/3")
    etag = first.headers["ETag"]
    assert client.get("/v2/employees/3", headers={"If-None-Match": etag}).status_code == 304
    stale = client.patch("/v2/employees/3", json={"title": "Finance Director"}, headers={"If-Match": '"stale"'})
    assert stale.status_code == 412
    ok = client.patch("/v2/employees/3", json={"title": "Finance Director"}, headers={"If-Match": etag})
    assert ok.status_code == 200


def test_idempotency_key(client):
    key = uuid.uuid4().hex
    body = new_employee(email=unique_email())
    first = client.post("/v2/employees", json=body, headers={"Idempotency-Key": key})
    again = client.post("/v2/employees", json=body, headers={"Idempotency-Key": key})
    assert first.status_code == again.status_code == 201
    assert first.json()["id"] == again.json()["id"]
    assert again.headers["Idempotent-Replayed"] == "true"
    other = client.post("/v2/employees", json=new_employee(email=unique_email()), headers={"Idempotency-Key": key})
    assert other.status_code == 422  # same key, different body
    client.delete(f"/v2/employees/{first.json()['id']}")
