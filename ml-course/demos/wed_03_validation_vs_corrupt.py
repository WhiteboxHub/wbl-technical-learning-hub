"""Wednesday Demo 3: Malformed input rejected by Pydantic (422) vs valid prediction (200).

Shows why schema validation prevents silent model corruption.
Live variation: --amount -50 (negative money) vs --amount 120.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from fraud_system.serve import app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--amount", type=float, default=-50.0, help="Live variation: try 120.0 vs -50.0")
    args = parser.parse_args()

    print("\n=== WEDNESDAY DEMO 3: VALIDATION BOUNDARY (422 VS 200) ===")
    bad_payload = {
        "amount": args.amount,
        "hour_of_day": 27,  # invalid hour
        "merchant_risk_score": 0.5,
        "tx_velocity_24h": 2,
        "distance_from_home_km": 10.0,
        "is_international": 0,
        "card_present": 1,
        "account_age_days": 300,
    }
    good_payload = {**bad_payload, "amount": 120.0, "hour_of_day": 14}
    with TestClient(app) as client:
        r_bad = client.post("/v1/predict", json=bad_payload)
        r_good = client.post("/v1/predict", json=good_payload)
        print(f"Malformed input -> HTTP {r_bad.status_code}: {r_bad.json()['detail']}")
        print(f"Valid input     -> HTTP {r_good.status_code}: {r_good.json()}")
    print("LIVE VARIATION: pass `--amount 120` (still fails on hour_of_day=27!) to inspect field-level errors.")


if __name__ == "__main__":
    main()
