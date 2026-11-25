"""Parameterized Fraud Detection training with MLflow tracking and Registry support."""
import argparse
import hashlib
import json
import os
import subprocess
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import yaml
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from .data_gen import generate_transactions
from .features import ENGINEERED_FEATURES, RAW_FEATURES, prepare_xy


def _git_sha() -> str:
    try:
        return subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def _file_sha256(path: Path) -> str:
    if not path.exists():
        return "none"
    return hashlib.sha256(path.read_bytes()).hexdigest()[:12]


def _compute_reference_stats(df: pd.DataFrame) -> dict:
    """Capture baseline distributions (bin edges + quantiles) for production drift detection."""
    stats = {"n_rows": int(len(df)), "fraud_rate": float(df["is_fraud"].mean()), "features": {}}
    for col in RAW_FEATURES:
        vals = df[col].astype(float).to_numpy()
        edges = np.unique(np.quantile(vals, np.linspace(0, 1, 11)))
        if len(edges) < 3:
            edges = np.linspace(float(vals.min()), float(vals.max()) + 1e-6, 6)
        hist, _ = np.histogram(vals, bins=edges)
        stats["features"][col] = {
            "mean": float(vals.mean()),
            "std": float(vals.std()),
            "edges": [float(x) for x in edges],
            "expected_pct": [float(max(c, 1) / max(hist.sum(), 1)) for c in hist],
            "sample": [float(x) for x in vals[:500]],
        }
    return stats


def _try_log_mlflow(
    cfg: dict,
    params: dict,
    metrics: dict,
    artifacts_dir: Path,
    pipeline: Pipeline,
    register: bool,
    promote_stage: str | None,
) -> str | None:
    """Log run to MLflow if mlflow is installed; returns run_id or None."""
    try:
        import mlflow
        import mlflow.sklearn
        from mlflow.tracking import MlflowClient
    except ImportError:
        return None

    tracking_uri = os.getenv("MLFLOW_TRACKING_URI") or Path("mlruns").resolve().as_uri()
    mlflow.set_tracking_uri(tracking_uri)
    mlflow.set_experiment(cfg.get("mlflow", {}).get("experiment_name", "fraud-detection-week2"))

    with mlflow.start_run() as run:
        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.set_tag("git_sha", params.get("git_sha", "unknown"))
        mlflow.set_tag("data_sha256", params.get("data_sha256", "none"))
        mlflow.log_artifacts(str(artifacts_dir), artifact_path="reports")
        mlflow.sklearn.log_model(pipeline, artifact_path="model")

        if register:
            model_name = cfg.get("mlflow", {}).get("registered_model_name", "fraud-detector")
            mv = mlflow.register_model(f"runs:/{run.info.run_id}/model", model_name)
            client = MlflowClient()
            if promote_stage:
                # Set alias (MLflow 2.9+/3.x) and transition stage if supported
                try:
                    client.set_registered_model_alias(model_name, promote_stage.lower(), mv.version)
                except Exception:
                    pass
                try:
                    client.transition_model_version_stage(
                        name=model_name, version=mv.version, stage=promote_stage, archive_existing_versions=True
                    )
                except Exception:
                    pass
        return run.info.run_id


def train_and_save(
    data_path: Path,
    params_path: Path,
    artifacts_dir: Path = Path("artifacts"),
    c_override: float | None = None,
    threshold_override: float | None = None,
    register: bool = False,
    promote_stage: str | None = None,
) -> dict:
    """Train the LogisticRegression fraud model, persist artifacts, and optionally log to MLflow."""
    cfg = yaml.safe_load(params_path.read_text(encoding="utf-8")) if params_path.exists() else {}
    data_cfg = cfg.get("data", {})
    model_cfg = cfg.get("model", {})

    if not data_path.exists():
        data_path.parent.mkdir(parents=True, exist_ok=True)
        generate_transactions(
            n_rows=int(data_cfg.get("n_rows", 2000)),
            seed=int(data_cfg.get("random_state", 42)),
            version=str(data_cfg.get("version", "v1")),
        ).to_csv(data_path, index=False)

    df = pd.read_csv(data_path)
    X, y = prepare_xy(df)

    test_size = float(data_cfg.get("test_size", 0.2))
    seed = int(data_cfg.get("random_state", 42))
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=seed, stratify=y)

    c_val = float(c_override if c_override is not None else model_cfg.get("C", 1.0))
    max_iter = int(model_cfg.get("max_iter", 500))
    raw_cw = model_cfg.get("class_weight", None)
    class_weight = None if raw_cw in (None, "null", "none", "None") else raw_cw
    threshold = float(threshold_override if threshold_override is not None else model_cfg.get("threshold", 0.35))

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(C=c_val, max_iter=max_iter, class_weight=class_weight, random_state=seed)),
        ]
    )
    pipeline.fit(X_train, y_train)

    probs = pipeline.predict_proba(X_test)[:, 1]
    preds = (probs >= threshold).astype(int)

    metrics = {
        "precision": round(float(precision_score(y_test, preds, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, preds, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, preds, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, probs)), 4),
        "pr_auc": round(float(average_precision_score(y_test, probs)), 4),
    }
    logged_params = {
        "C": c_val,
        "max_iter": max_iter,
        "class_weight": str(class_weight),
        "threshold": threshold,
        "n_features": len(ENGINEERED_FEATURES),
        "n_train": len(X_train),
        "n_test": len(X_test),
        "git_sha": _git_sha(),
        "data_sha256": _file_sha256(data_path),
    }

    artifacts_dir.mkdir(parents=True, exist_ok=True)
    bundle = {
        "pipeline": pipeline,
        "threshold": threshold,
        "version": f"v1-{logged_params['data_sha256'][:6]}-C{c_val}",
        "params": logged_params,
        "metrics": metrics,
        "features": ENGINEERED_FEATURES,
    }
    joblib.dump(bundle, artifacts_dir / "model.joblib")
    (artifacts_dir / "metrics.json").write_text(json.dumps({"params": logged_params, "metrics": metrics}, indent=2), encoding="utf-8")
    (artifacts_dir / "reference_stats.json").write_text(json.dumps(_compute_reference_stats(df), indent=2), encoding="utf-8")

    run_id = _try_log_mlflow(cfg, logged_params, metrics, artifacts_dir, pipeline, register, promote_stage)
    return {"run_id": run_id, "version": bundle["version"], "params": logged_params, "metrics": metrics}


def main() -> None:
    parser = argparse.ArgumentParser(description="Train Fraud Detection model.")
    parser.add_argument("--data", type=Path, default=Path("data/transactions.csv"))
    parser.add_argument("--params", type=Path, default=Path("params.yaml"))
    parser.add_argument("--artifacts", type=Path, default=Path("artifacts"))
    parser.add_argument("--C", type=float, default=None, dest="c_val")
    parser.add_argument("--threshold", type=float, default=None)
    parser.add_argument("--register", action="store_true")
    parser.add_argument("--promote", choices=["Staging", "Production"], default=None)
    args = parser.parse_args()

    result = train_and_save(
        data_path=args.data,
        params_path=args.params,
        artifacts_dir=args.artifacts,
        c_override=args.c_val,
        threshold_override=args.threshold,
        register=args.register,
        promote_stage=args.promote,
    )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
