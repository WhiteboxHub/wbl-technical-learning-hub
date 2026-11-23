"""Module 4 auth tests: tokens, 401 vs 403, and who can see what."""
import jwt
import pytest

PW = "pytest-only-password"


@pytest.fixture()
def auth_on(monkeypatch):
    monkeypatch.setenv("AUTH", "1")


def token(client, user, password=PW):
    return client.post("/v2/auth/token", data={"username": user, "password": password})


def bearer(client, user):
    return {"Authorization": "Bearer " + token(client, user).json()["access_token"]}


def test_login_ok_and_bad_password(client, auth_on):
    assert token(client, "hr_admin").status_code == 200
    assert token(client, "hr_admin", "wrong").status_code == 401
    assert token(client, "nobody").status_code == 401


def test_jwt_claims(client, auth_on):
    t = token(client, "manager").json()["access_token"]
    claims = jwt.decode(t, options={"verify_signature": False})
    assert claims["role"] == "manager" and claims["dept"] == 2 and claims["emp"] == 2
    assert {"iss", "aud", "sub", "exp", "iat"} <= claims.keys()


def test_401_without_or_with_bad_token(client, auth_on):
    assert client.get("/v2/employees/7").status_code == 401
    assert client.get("/v2/employees/7", headers={"Authorization": "Bearer nonsense"}).status_code == 401
    good = token(client, "hr_admin").json()["access_token"]
    assert client.get("/v2/employees/7", headers={"Authorization": "Bearer " + good[:-1] + "X"}).status_code == 401


def test_expired_token_is_401(client, auth_on, monkeypatch):
    monkeypatch.setenv("TOKEN_TTL", "-5")
    t = token(client, "hr_admin").json()["access_token"]
    r = client.get("/v2/employees/7", headers={"Authorization": "Bearer " + t})
    assert r.status_code == 401 and "expired" in r.json()["detail"]


def test_salary_visibility_by_role(client, auth_on):
    hr, mgr, emp = (bearer(client, u) for u in ("hr_admin", "manager", "employee"))
    assert client.get("/v2/employees/7", headers=hr).json()["salary"] > 0
    assert client.get("/v2/employees/7", headers=mgr).status_code == 200      # manager of Engineering
    assert client.get("/v2/employees/7", headers=emp).status_code == 200      # own record
    assert client.get("/v2/employees/2", headers=emp).status_code == 403      # someone else's
    assert client.get("/v2/employees/1", headers=mgr).status_code == 403      # other department


def test_lists_are_scoped_by_role(client, auth_on):
    assert len(client.get("/v2/employees?limit=100", headers=bearer(client, "hr_admin")).json()) >= 20
    assert {e["department_id"] for e in client.get("/v2/employees?limit=100", headers=bearer(client, "manager")).json()} == {2}
    assert [e["id"] for e in client.get("/v2/employees?limit=100", headers=bearer(client, "employee")).json()] == [7]


def test_only_hr_admin_can_write(client, auth_on):
    assert client.delete("/v2/employees/20", headers=bearer(client, "manager")).status_code == 403
    assert client.patch("/v2/employees/20", json={"title": "x"}, headers=bearer(client, "employee")).status_code == 403
    assert client.post("/v2/departments", json={"name": "Nope", "location": "x"}, headers=bearer(client, "manager")).status_code == 403


def test_basic_demo(client):
    assert client.get("/demo/basic").status_code == 401
    assert client.get("/demo/basic", auth=("hr_admin", PW)).status_code == 200
    assert client.get("/demo/basic", auth=("hr_admin", "bad")).status_code == 401


def test_auth_off_by_default(client):
    assert client.get("/v2/employees/7").status_code == 200
