"""Thursday Demo 1: Synthetic drift injected into a live stream until the alarm fires.

Live variation: --psi-alert 0.50 to raise the sensitivity threshold.
"""
import argparse
import json
import os
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fraud_system.data_gen import generate_transactions
from fraud_system.monitor import DriftMonitor
from fraud_system.train import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--psi-alert", type=float, default=0.25, help="Live variation: PSI alert threshold")
    args = parser.parse_args()

    print("\n=== THURSDAY DEMO 1: LIVE STREAM DRIFT DETECTION ===")
    art_dir = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))
    data_path = Path(os.getenv("DATA_PATH", "data/transactions.csv"))
    ref_path = art_dir / "reference_stats.json"
    if not ref_path.exists():
        train_and_save(data_path, Path("params.yaml"), artifacts_dir=art_dir)
    ref_stats = json.loads(ref_path.read_text(encoding="utf-8"))
    monitor = DriftMonitor(ref_stats, psi_alert=args.psi_alert)

    for step, drifted in [(1, False), (2, False), (3, True), (4, True)]:
        batch = generate_transactions(n_rows=80, seed=100 + step, data_drift=drifted)
        for row in batch.to_dict(orient="records"):
            monitor.record_prediction(row, prob=0.2, pred=0, latency_ms=4.0)
        summary = monitor.summary()
        tag = "DRIFTED" if drifted else "CLEAN  "
        print(f"Batch {step} ({tag}) | status={summary['overall_status']:7s} | max_psi={summary['max_psi']:.4f} | alerts={summary['alerts']}")
    print("LIVE VARIATION: re-run with `--psi-alert 0.50` to see how threshold choice shifts alarm timing.")


if __name__ == "__main__":
    main()
