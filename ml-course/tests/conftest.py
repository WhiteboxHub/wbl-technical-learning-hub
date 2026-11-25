import tempfile
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

from fraud_system import serve
from fraud_system.data_gen import generate_transactions
from fraud_system.train import train_and_save


@pytest.fixture(scope="session")
def test_workspace(tmp_path_factory):
    root = tmp_path_factory.mktemp("fraud_ws")
    data_path = root / "transactions.csv"
    art_dir = root / "artifacts"
    fault_file = root / ".fault_state.json"
    fault_file.write_text("{}", encoding="utf-8")

    import os
    old_uri = os.environ.get("MLFLOW_TRACKING_URI")
    os.environ["MLFLOW_TRACKING_URI"] = (root / "mlruns").as_uri()
    try:
        generate_transactions(n_rows=800, seed=42, version="v1").to_csv(data_path, index=False)
        train_and_save(data_path=data_path, params_path=Path("params.yaml"), artifacts_dir=art_dir)
    finally:
        if old_uri is None:
            os.environ.pop("MLFLOW_TRACKING_URI", None)
        else:
            os.environ["MLFLOW_TRACKING_URI"] = old_uri
    return {"root": root, "data": data_path, "artifacts": art_dir, "fault": fault_file, "mlruns": (root / "mlruns").as_uri()}


@pytest.fixture()
def client(test_workspace, monkeypatch):
    monkeypatch.setattr(serve, "ARTIFACTS_DIR", test_workspace["artifacts"])
    monkeypatch.setattr(serve, "DATA_PATH", test_workspace["data"])
    monkeypatch.setattr(serve, "FAULT_STATE", test_workspace["fault"])
    test_workspace["fault"].write_text("{}", encoding="utf-8")
    serve._state.clear()
    with TestClient(serve.app) as c:
        yield c
    test_workspace["fault"].write_text("{}", encoding="utf-8")


def sample_tx(**overrides):
    tx = {
        "amount": 1850.0,
        "hour_of_day": 2,
        "merchant_risk_score": 0.85,
        "tx_velocity_24h": 5,
        "distance_from_home_km": 220.0,
        "is_international": 1,
        "card_present": 0,
        "account_age_days": 60,
    }
    tx.update(overrides)
    return tx
