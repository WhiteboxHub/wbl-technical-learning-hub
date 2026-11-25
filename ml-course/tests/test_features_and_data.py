from pathlib import Path

from fraud_system.data_gen import generate_transactions
from fraud_system.evaluate import evaluate_metrics
from fraud_system.features import ENGINEERED_FEATURES, engineer_features
from fraud_system.train import train_and_save


def test_deterministic_data_generation():
    df1 = generate_transactions(n_rows=300, seed=42, version="v1")
    df2 = generate_transactions(n_rows=300, seed=42, version="v1")
    assert df1.equals(df2)
    assert set(df1["is_fraud"].unique()) <= {0, 1}


def test_feature_engineering_parity():
    df = generate_transactions(n_rows=20, seed=7)
    feats = engineer_features(df)
    assert list(feats.columns) == ENGINEERED_FEATURES
    assert (feats["log_amount"] > 0).all()
    assert set(feats["is_night"].unique()) <= {0, 1}


def test_train_and_evaluate_pipeline(tmp_path, monkeypatch):
    monkeypatch.setenv("MLFLOW_TRACKING_URI", (tmp_path / "mlruns").as_uri())
    data_path = tmp_path / "tx.csv"
    art_dir = tmp_path / "artifacts"
    eval_path = tmp_path / "eval.json"

    generate_transactions(n_rows=1000, seed=42, version="v1").to_csv(data_path, index=False)
    res = train_and_save(data_path=data_path, params_path=Path("params.yaml"), artifacts_dir=art_dir)

    assert (art_dir / "model.joblib").exists()
    assert (art_dir / "metrics.json").exists()
    assert (art_dir / "reference_stats.json").exists()
    assert res["metrics"]["roc_auc"] > 0.70

    report = evaluate_metrics(art_dir / "metrics.json", Path("params.yaml"), eval_path)
    assert eval_path.exists()
    assert "passed" in report and "recommendation" in report
