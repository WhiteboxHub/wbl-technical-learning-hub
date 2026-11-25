import os
import subprocess
import sys

from .conftest import sample_tx


def test_fault_injection_bad_schema_and_latency(client, test_workspace):
    test_workspace["fault"].write_text('{"fault":"bad-schema"}', encoding="utf-8")
    assert client.get("/health").status_code == 503
    assert client.post("/v1/predict", json=sample_tx()).status_code == 500

    test_workspace["fault"].write_text('{"fault":"latency-spike"}', encoding="utf-8")
    assert client.get("/health").status_code == 200
    r = client.post("/v1/predict", json=sample_tx())
    assert r.status_code == 200
    assert r.json()["latency_ms"] >= 200.0


def test_offline_demo_scripts_run_cleanly(tmp_path):
    env = {
        **os.environ,
        "PYTHONPATH": ".",
        "ARTIFACTS_DIR": str(tmp_path / "artifacts"),
        "DATA_PATH": str(tmp_path / "transactions.csv"),
        "FAULT_STATE_PATH": str(tmp_path / ".fault_state.json"),
        "MLFLOW_TRACKING_URI": (tmp_path / "mlruns").as_uri(),
    }
    for script in [
        "demos/mon_01_unreproducible.py",
        "demos/wed_01_fastapi_service.py",
        "demos/wed_03_validation_vs_corrupt.py",
        "demos/thu_01_drift_stream.py",
        "demos/thu_03_alert_tuning.py",
    ]:
        res = subprocess.run([sys.executable, script], capture_output=True, text=True, timeout=30, env=env)
        assert res.returncode == 0, f"{script} failed: {res.stderr}"
