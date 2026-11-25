from .conftest import sample_tx


def test_health_and_dashboard(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
    assert client.get("/").status_code == 200


def test_model_info(client):
    r = client.get("/v1/model-info")
    assert r.status_code == 200
    body = r.json()
    assert body["threshold"] > 0
    assert "log_amount" in body["features"]


def test_predict_valid_and_validation_422(client):
    good = client.post("/v1/predict", json=sample_tx())
    assert good.status_code == 200
    data = good.json()
    assert 0.0 <= data["fraud_probability"] <= 1.0
    assert data["risk_band"] in {"LOW", "MEDIUM", "HIGH"}

    bad = client.post("/v1/predict", json=sample_tx(amount=-10, hour_of_day=29))
    assert bad.status_code == 422


def test_rollback_updates_threshold_and_restores(client):
    r1 = client.post("/v1/rollback", json={"threshold": 0.60, "restore_baseline": True})
    assert r1.status_code == 200
    assert r1.json()["threshold"] == 0.60

    r2 = client.post("/v1/rollback", json={"restore_baseline": True})
    assert r2.status_code == 200
    assert r2.json()["threshold"] == 0.35


def test_prometheus_metrics_endpoint(client):
    client.post("/v1/predict", json=sample_tx())
    m = client.get("/metrics")
    assert m.status_code == 200
    assert "fraud_requests_total" in m.text
    assert "fraud_max_psi" in m.text
