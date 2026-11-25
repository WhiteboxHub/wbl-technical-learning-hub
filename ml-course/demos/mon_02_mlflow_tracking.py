"""Monday Demo 2: MLflow tracking on real Fraud Detection runs.

Logs two runs (different C / threshold) with params, metrics, and artifacts so the
class can compare them side by side in the MLflow UI or terminal.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fraud_system.train import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--c1", type=float, default=0.1)
    parser.add_argument("--c2", type=float, default=2.0)
    parser.add_argument("--threshold", type=float, default=0.35, help="Live variation: try 0.20 vs 0.60")
    args = parser.parse_args()

    print("\n=== MONDAY DEMO 2: MLFLOW EXPERIMENT TRACKING ===")
    r1 = train_and_save(Path("data/transactions.csv"), Path("params.yaml"), c_override=args.c1, threshold_override=args.threshold)
    r2 = train_and_save(Path("data/transactions.csv"), Path("params.yaml"), c_override=args.c2, threshold_override=args.threshold)

    for label, res in [("Run 1", r1), ("Run 2", r2)]:
        m = res["metrics"]
        print(f"{label} | run_id={res['run_id'] or 'local-only'} | C={res['params']['C']} | thr={res['params']['threshold']} "
              f"| recall={m['recall']} | precision={m['precision']} | f1={m['f1']}")
    print("LIVE VARIATION: re-run with `--threshold 0.20` to watch recall rise and precision drop.")


if __name__ == "__main__":
    main()
