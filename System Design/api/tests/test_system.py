import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    assert "instance_id" in data

def test_create_and_redirect_short_url():
    # 1. Create short URL
    create_res = client.post("/api/shorten", json={"url": "https://example.com/system-design"})
    assert create_res.status_code in [201, 202]
    code = create_res.json()["short_code"]

    # 2. Follow redirect (disable auto-follow to check 302)
    redirect_res = client.get(f"/r/{code}", follow_redirects=False)
    assert redirect_res.status_code == 302
    assert redirect_res.headers["location"] == "https://example.com/system-design"
    assert "X-Cache" in redirect_res.headers

def test_metrics_endpoint():
    res = client.get("/api/metrics")
    assert res.status_code == 200
    data = res.json()
    assert "cache_hits" in data
    assert "hit_ratio_percent" in data
