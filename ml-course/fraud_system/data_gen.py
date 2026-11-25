"""Deterministic synthetic credit-card transaction dataset generator.

Supports clean baseline snapshots (v1, v2) for DVC versioning demos and
drifted production streams (data drift and concept drift) for monitoring demos.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd


def generate_transactions(
    n_rows: int = 2000,
    seed: int = 42,
    version: str = "v1",
    data_drift: bool = False,
    concept_drift: bool = False,
) -> pd.DataFrame:
    """Generate synthetic credit-card transactions with reproducible fraud labels."""
    rng = np.random.default_rng(seed)

    # v2 simulates a new quarter with higher average amounts and more international volume
    amount_scale = 3.8 if (version == "v1" and not data_drift) else (4.1 if version == "v2" else 5.2)
    intl_prob = 0.08 if (version == "v1" and not data_drift) else (0.14 if version == "v2" else 0.42)
    dist_scale = 18.0 if not data_drift else 95.0

    amount = np.round(np.exp(rng.normal(amount_scale, 0.95, n_rows)), 2)
    hour_of_day = rng.integers(0, 24, size=n_rows)
    merchant_risk_score = np.round(rng.beta(2.0, 5.0 if not data_drift else 2.2, n_rows), 4)
    tx_velocity_24h = rng.poisson(2.2 if not data_drift else 5.5, n_rows) + 1
    distance_from_home_km = np.round(rng.exponential(dist_scale, n_rows), 2)
    is_international = rng.binomial(1, intl_prob, n_rows)
    card_present = rng.binomial(1, 0.72 if not data_drift else 0.35, n_rows)
    account_age_days = rng.integers(5, 2500, size=n_rows)

    if not concept_drift:
        # Standard fraud relationship: high amount + high merchant risk + international + night + velocity
        logit = (
            -4.6
            + 0.75 * np.log1p(amount) / 4.0
            + 3.1 * merchant_risk_score
            + 0.38 * np.maximum(tx_velocity_24h - 3, 0)
            + 0.012 * np.minimum(distance_from_home_km, 250.0)
            + 1.35 * is_international
            - 0.95 * card_present
            + 0.65 * ((hour_of_day < 5) | (hour_of_day >= 23)).astype(float)
            - 0.0005 * account_age_days
        )
    else:
        # Concept drift: attackers switch to low-amount, daytime, card-present micro-testing on aged accounts
        logit = (
            -2.4
            - 0.65 * np.log1p(amount) / 4.0
            + 1.2 * merchant_risk_score
            + 0.75 * np.maximum(tx_velocity_24h - 1, 0)
            + 1.45 * card_present
            + 0.85 * ((hour_of_day >= 9) & (hour_of_day <= 17)).astype(float)
            + 0.0004 * account_age_days
        )

    probs = 1.0 / (1.0 + np.exp(-logit))
    is_fraud = rng.binomial(1, probs)

    return pd.DataFrame(
        {
            "amount": amount,
            "hour_of_day": hour_of_day,
            "merchant_risk_score": merchant_risk_score,
            "tx_velocity_24h": tx_velocity_24h,
            "distance_from_home_km": distance_from_home_km,
            "is_international": is_international,
            "card_present": card_present,
            "account_age_days": account_age_days,
            "is_fraud": is_fraud,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic Fraud Detection dataset.")
    parser.add_argument("--version", choices=["v1", "v2"], default="v1")
    parser.add_argument("--n-rows", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--out", type=Path, default=Path("data/transactions.csv"))
    args = parser.parse_args()

    args.out.parent.mkdir(parents=True, exist_ok=True)
    df = generate_transactions(n_rows=args.n_rows, seed=args.seed, version=args.version)
    df.to_csv(args.out, index=False)
    fraud_rate = df["is_fraud"].mean() * 100
    print(f"Generated {len(df)} rows ({args.version}) -> {args.out} (fraud_rate={fraud_rate:.2f}%)")


if __name__ == "__main__":
    main()
