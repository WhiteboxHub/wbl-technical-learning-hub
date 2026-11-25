"""Monday Demo 3: Model Registry promotion from Staging to Production.

Registers a Fraud Detection model in MLflow Registry and walks through Staging -> Production
with lineage metadata. Live variation: --stage Staging to hold before Production.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fraud_system.train import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["Staging", "Production"], default="Production")
    args = parser.parse_args()

    print("\n=== MONDAY DEMO 3: MODEL REGISTRY PROMOTION ===")
    res = train_and_save(
        Path("data/transactions.csv"),
        Path("params.yaml"),
        register=True,
        promote_stage=args.stage,
    )
    print(f"Model version : {res['version']}")
    print(f"MLflow run_id : {res['run_id'] or '(install mlflow to enable server registry)'}")
    print(f"Target stage  : {args.stage}")
    print(f"Lineage tags  : git_sha={res['params']['git_sha']}, data_sha256={res['params']['data_sha256']}")
    print("LIVE VARIATION: re-run with `--stage Staging` to simulate pre-production validation hold.")


if __name__ == "__main__":
    main()
