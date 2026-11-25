"""Tuesday Demo 1: Version a dataset with DVC and roll it back byte-for-byte.

Creates an isolated sandbox folder in /tmp (or %TEMP%), initializes Git + DVC,
commits dataset v1, updates to v2, and rolls back to v1 proving exact byte hash match.
"""
import argparse
import hashlib
import importlib.util
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fraud_system.data_gen import generate_transactions


def _run(cmd: list[str], cwd: Path) -> None:
    env = os.environ.copy()
    env["PATH"] = str(Path(sys.executable).parent) + os.pathsep + env.get("PATH", "")
    resolved = [sys.executable, "-m", "dvc", *cmd[1:]] if cmd[0] == "dvc" else cmd
    subprocess.run(resolved, cwd=cwd, env=env, check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows-v2", type=int, default=2500, help="Live variation: change v2 row count")
    args = parser.parse_args()

    print("\n=== TUESDAY DEMO 1: DVC DATA VERSIONING & ROLLBACK ===")
    if importlib.util.find_spec("dvc") is None:
        print("DVC is not installed in this Python env. Run inside Docker or install `dvc` via requirements.txt.")
        return

    with tempfile.TemporaryDirectory(prefix="dvc_demo1_") as tmp:
        root = Path(tmp)
        remote = root / "dvc_remote"
        remote.mkdir()
        _run(["git", "init"], root)
        _run(["git", "config", "user.email", "demo@whitebox.local"], root)
        _run(["git", "config", "user.name", "Demo"], root)
        _run(["dvc", "init"], root)
        _run(["dvc", "remote", "add", "-d", "localstore", str(remote)], root)

        csv_path = root / "transactions.csv"
        generate_transactions(n_rows=1000, seed=42, version="v1").to_csv(csv_path, index=False)
        h1 = _sha256(csv_path)
        _run(["dvc", "add", "transactions.csv"], root)
        _run(["git", "add", "transactions.csv.dvc", ".gitignore", ".dvc"], root)
        _run(["git", "commit", "-m", "data v1"], root)
        print(f"Committed v1 : rows=1000 | sha256={h1}")

        generate_transactions(n_rows=args.rows_v2, seed=42, version="v2").to_csv(csv_path, index=False)
        h2 = _sha256(csv_path)
        _run(["dvc", "add", "transactions.csv"], root)
        _run(["git", "add", "transactions.csv.dvc"], root)
        _run(["git", "commit", "-m", "data v2"], root)
        print(f"Committed v2 : rows={args.rows_v2} | sha256={h2}")

        _run(["git", "checkout", "HEAD~1", "transactions.csv.dvc"], root)
        _run(["dvc", "checkout"], root)
        h_back = _sha256(csv_path)
        print(f"Rolled back  : sha256={h_back} | byte_match_v1={h_back == h1}")
        print("LIVE VARIATION: pass `--rows-v2 3500` to observe hash change and exact v1 restoration.")


if __name__ == "__main__":
    main()
