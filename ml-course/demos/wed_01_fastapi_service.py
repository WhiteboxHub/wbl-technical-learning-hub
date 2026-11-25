"""Wednesday Demo 1: Baseline Fraud model wrapped in FastAPI (in-process TestClient).

Live variation: pass --amount 4500 --risk 0.92 to test a high-risk transaction.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from fraud_system.serve import app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float, default=85.0)
    parser.add_argument("--risk", type=float, default=0.18)
    args = parser.parse_args()

    print("\n=== WEDNESDAY DEMO 1: FASTAPI MODEL SERVICE ===")
    payload = {
        "amount": args.amount,
        "hour_of_day": 14,
        "merchant_risk_score": args.risk,
        "tx_velocity_24h": 1,
        "distance_from_home_km": 5.0,
        "is_international": 0,
        "card_present": 1,
        "account_age_days": 800,
    }
    with TestClient(app) as client:
        h = client.get("/health")
        p = client.post("/v1/predict", json=payload)
        print(f"GET  /health     -> {h.status_code} {h.json()}")
        print(f"POST /v1/predict -> {p.status_code} {p.json()}")
    print("LIVE VARIATION: re-run with `--amount 4500 --risk 0.92` to flip is_fraud False -> True.")


if __name__ == "__main__":
    main()
