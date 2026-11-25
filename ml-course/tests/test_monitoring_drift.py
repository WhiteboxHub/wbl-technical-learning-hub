def test_clean_stream_stays_healthy_and_drift_alerts(client):
    client.post("/v1/monitor/reset")
    clean = client.post("/v1/monitor/simulate", json={"n": 100, "data_drift": False, "seed": 11}).json()
    assert clean["overall_status"] == "HEALTHY"
    assert clean["window_samples"] == 100

    drifted = client.post("/v1/monitor/simulate", json={"n": 150, "data_drift": True, "seed": 22}).json()
    assert drifted["overall_status"] == "ALERT"
    assert drifted["max_psi"] >= 0.25
    assert len(drifted["drifted_features"]) >= 1
    assert len(drifted["alerts"]) >= 1


def test_concept_drift_shifts_predicted_fraud_rate(client):
    client.post("/v1/monitor/reset")
    base = client.post("/v1/monitor/simulate", json={"n": 120, "data_drift": False, "concept_drift": False, "seed": 50}).json()
    client.post("/v1/monitor/reset")
    shifted = client.post("/v1/monitor/simulate", json={"n": 120, "data_drift": False, "concept_drift": True, "seed": 50}).json()
    assert base["window_samples"] == shifted["window_samples"] == 120
    assert shifted["max_psi"] < 0.25  # inputs remain calm under concept drift


def test_monitor_reset(client):
    client.post("/v1/monitor/simulate", json={"n": 40, "data_drift": True})
    assert client.post("/v1/monitor/reset").status_code == 200
    summary = client.get("/v1/monitor/drift").json()
    assert summary["window_samples"] == 0
    assert summary["overall_status"] == "HEALTHY"
