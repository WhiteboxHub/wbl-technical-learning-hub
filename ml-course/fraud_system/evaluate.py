"""Evaluate trained Fraud Detection metrics against the promotion gate."""
import argparse
import json
from pathlib import Path

import yaml


def evaluate_metrics(metrics_path: Path, params_path: Path, out_path: Path) -> dict:
    payload = json.loads(metrics_path.read_text(encoding="utf-8"))
    cfg = yaml.safe_load(params_path.read_text(encoding="utf-8")) if params_path.exists() else {}
    min_recall = float(cfg.get("monitoring", {}).get("min_recall_gate", 0.70))

    metrics = payload["metrics"]
    passed = metrics["recall"] >= min_recall
    report = {
        "passed": passed,
        "min_recall_gate": min_recall,
        "observed_recall": metrics["recall"],
        "observed_f1": metrics["f1"],
        "observed_pr_auc": metrics["pr_auc"],
        "recommendation": "PROMOTE" if passed else "HOLD",
    }
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate trained model against gate.")
    parser.add_argument("--metrics", type=Path, default=Path("artifacts/metrics.json"))
    parser.add_argument("--params", type=Path, default=Path("params.yaml"))
    parser.add_argument("--out", type=Path, default=Path("artifacts/eval_report.json"))
    args = parser.parse_args()

    report = evaluate_metrics(args.metrics, args.params, args.out)
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
