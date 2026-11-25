"""Tuesday Demo 3: Solving the silent-edit mystery with data hashes & lineage.

Shows what happens when a CSV is silently modified between training runs and how
comparing data SHA-256 + metrics proves the dataset changed underneath the code.
"""
import argparse
import hashlib
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fraud_system.data_gen import generate_transactions
from fraud_system.train import train_and_save


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--silent-edit", action="store_true", default=True, help="Simulate silent CSV edit")
    parser.add_argument("--no-edit", dest="silent_edit", action="store_false", help="Live variation: keep clean data")
    args = parser.parse_args()

    print("\n=== TUESDAY DEMO 3: THE SILENT-EDIT MYSTERY ===")
    with tempfile.TemporaryDirectory(prefix="lineage_demo_") as tmp:
        root = Path(tmp)
        csv_path = root / "transactions.csv"
        generate_transactions(n_rows=1500, seed=42, version="v1").to_csv(csv_path, index=False)
        r1 = train_and_save(csv_path, Path("params.yaml"), artifacts_dir=root / "art1")

        if args.silent_edit:
            # Someone edits data/transactions.csv without changing code or telling the team
            generate_transactions(n_rows=1500, seed=42, version="v2", data_drift=True).to_csv(csv_path, index=False)

        r2 = train_and_save(csv_path, Path("params.yaml"), artifacts_dir=root / "art2")
        print(f"Run 1 | data_sha256={r1['params']['data_sha256']} | recall={r1['metrics']['recall']} | f1={r1['metrics']['f1']}")
        print(f"Run 2 | data_sha256={r2['params']['data_sha256']} | recall={r2['metrics']['recall']} | f1={r2['metrics']['f1']}")
        if r1["params"]["data_sha256"] != r2["params"]["data_sha256"]:
            print("MYSTERY SOLVED: Code & params were identical, but data_sha256 changed! DVC catches this before training.")
        else:
            print("DATA CLEAN: data_sha256 matched — metrics are identical.")
        print("LIVE VARIATION: pass `--no-edit` to verify identical hashes & metrics.")


if __name__ == "__main__":
    main()
