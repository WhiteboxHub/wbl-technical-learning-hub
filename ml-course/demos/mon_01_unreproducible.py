"""Monday Demo 1: The unreproducible experiment.

Runs training WITHOUT fixed seeds, WITHOUT logged split/parameters, and compares
two consecutive runs. Live variation: pass --fix-seed 42 to show seed control.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from fraud_system.data_gen import generate_transactions
from fraud_system.features import prepare_xy


def run_untracked(label: str, seed: int | None) -> None:
    # Without fixed data & split seeds, every run silently shifts
    actual_seed = int(np.random.default_rng().integers(1, 10000)) if seed is None else seed
    df = generate_transactions(n_rows=1000, seed=actual_seed)
    X, y = prepare_xy(df)
    X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, random_state=seed)
    clf = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("clf", LogisticRegression(max_iter=1500, class_weight="balanced")),
        ]
    )
    clf.fit(X_tr, y_tr)
    probs = clf.predict_proba(X_te)[:, 1]
    preds = (probs >= 0.4).astype(int)
    print(f"[{label}] recall={recall_score(y_te, preds):.4f} | f1={f1_score(y_te, preds):.4f} | params=UNLOGGED")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix-seed", type=int, default=None, help="Live variation: set a fixed seed (e.g. 42)")
    args = parser.parse_args()

    print("\n=== MONDAY DEMO 1: THE LAB NOTEBOOK PROBLEM ===")
    run_untracked("Run A (Tuesday)", args.fix_seed)
    run_untracked("Run B (Rerun!) ", args.fix_seed)
    if args.fix_seed is None:
        print("RESULT: Numbers shifted and NOBODY recorded params, seed, or data version!")
        print("LIVE VARIATION: re-run with `--fix-seed 42` to compare.")
    else:
        print(f"RESULT: With seed={args.fix_seed}, both runs match — but still no central lab notebook!")


if __name__ == "__main__":
    main()
