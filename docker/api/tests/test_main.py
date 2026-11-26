from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture()
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_file = tmp_path / "manifest.db"
    monkeypatch.setenv("MANIFEST_DB_PATH", str(db_file))
    monkeypatch.setenv("REDIS_URL", "")
    return TestClient(app)


def test_health(client: TestClient) -> None:
    resp = client.get("/health")
    assert resp.status_code == 200
    body = resp.json()
    assert body["status"] == "ok"
    assert body["redis"] == "disabled"


def test_container_crud_and_stats(client: TestClient) -> None:
    create_resp = client.post(
        "/containers",
        json={
            "container_code": "mscu1234567",
            "cargo": "Server Racks",
            "origin_port": "Shenzhen",
            "destination_port": "Rotterdam",
            "weight_kg": 18200,
            "status": "docked",
        },
    )
    assert create_resp.status_code == 201
    created = create_resp.json()
    assert created["container_code"] == "MSCU1234567"
    cid = created["id"]

    # Duplicate container code returns 409
    dup_resp = client.post(
        "/containers",
        json={
            "container_code": "MSCU1234567",
            "cargo": "Duplicate",
            "origin_port": "Shenzhen",
            "destination_port": "Rotterdam",
            "weight_kg": 1000,
        },
    )
    assert dup_resp.status_code == 409

    # List & filter
    list_resp = client.get("/containers")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    # Patch status
    patch_resp = client.patch(f"/containers/{cid}", json={"status": "in_transit"})
    assert patch_resp.status_code == 200
    assert patch_resp.json()["status"] == "in_transit"

    # Stats
    stats_resp = client.get("/stats")
    assert stats_resp.status_code == 200
    assert stats_resp.json()["total_containers"] == 1
    assert stats_resp.json()["total_weight_kg"] == 18200

    # Delete
    del_resp = client.delete(f"/containers/{cid}")
    assert del_resp.status_code == 204
    assert client.get(f"/containers/{cid}").status_code == 404


def test_patch_validation_and_not_found(client: TestClient) -> None:
    create_resp = client.post(
        "/containers",
        json={
            "container_code": "MAEU9876543",
            "cargo": "Solar Panels",
            "origin_port": "Shanghai",
            "destination_port": "Hamburg",
            "weight_kg": 12000,
        },
    )
    assert create_resp.status_code == 201
    cid = create_resp.json()["id"]

    # Null-only or empty PATCH returns 400 instead of hitting SQLite NOT NULL 500
    assert client.patch(f"/containers/{cid}", json={}).status_code == 400
    assert client.patch(f"/containers/{cid}", json={"cargo": None}).status_code == 400

    # Non-existent container returns 404
    assert client.patch("/containers/99999", json={"status": "delivered"}).status_code == 404
    assert client.delete("/containers/99999").status_code == 404

    # Status filter returns matching containers only
    assert len(client.get("/containers?status_filter=docked").json()) == 1
    assert len(client.get("/containers?status_filter=delivered").json()) == 0
