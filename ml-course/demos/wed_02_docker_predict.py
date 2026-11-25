"""Wednesday Demo 2: Call the live Dockerized Fraud API over HTTP.

Live variation: --url http://localhost:8000 and --amount 3200.
"""
import argparse
import httpx


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default="http://localhost:8000")
    parser.add_argument("--amount", type=float, default=2400.0)
    args = parser.parse_args()

    print("\n=== WEDNESDAY DEMO 2: LIVE CONTAINER PREDICTION ===")
    tx = {
        "amount": args.amount,
        "hour_of_day": 1,
        "merchant_risk_score": 0.85,
        "tx_velocity_24h": 6,
        "distance_from_home_km": 410.0,
        "is_international": 1,
        "card_present": 0,
        "account_age_days": 45,
    }
    try:
        health = httpx.get(f"{args.url}/health", timeout=3.0)
        resp = httpx.post(f"{args.url}/v1/predict", json=tx, timeout=3.0)
        print(f"Health : {health.status_code} {health.json()}")
        print(f"Predict: {resp.status_code} {resp.json()}")
    except Exception as exc:
        print(f"Could not reach {args.url} ({exc}). Start container with `docker compose up -d --build`.")
    print("LIVE VARIATION: pass `--amount 25.0` to observe probability drop.")


if __name__ == "__main__":
    main()
