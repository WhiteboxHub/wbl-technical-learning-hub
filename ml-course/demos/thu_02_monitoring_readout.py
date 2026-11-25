"""Thursday Demo 2: Monitoring readout (inputs, outputs, latency, drift) via API.

Live variation: --concept-drift to show fraud rate & performance shifting even when inputs look calmer.
"""
import argparse
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi.testclient import TestClient

from fraud_system.serve import app


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-drift", action="store_true", default=None, help="Inject covariate/input drift")
    parser.add_argument("--concept-drift", action="store_true", default=False, help="Inject concept drift (calm inputs, shifted fraud rules)")
    args = parser.parse_args()

    use_data_drift = (not args.concept_drift) if args.data_drift is None else args.data_drift

    print("\n=== THURSDAY DEMO 2: MONITORING READOUT ===")
    with TestClient(app) as client:
        client.post("/v1/monitor/reset")
        report = client.post(
            "/v1/monitor/simulate",
            json={"n": 150, "data_drift": use_data_drift, "concept_drift": args.concept_drift, "seed": 77},
        ).json()
        print(f"Overall status  : {report['overall_status']}")
        print(f"Window samples  : {report['window_samples']}")
        print(f"Latency p50/p95 : {report['latency_p50_ms']}ms / {report['latency_p95_ms']}ms")
        print(f"Fraud rate live : {report['live_fraud_rate']} (ref: {report['ref_fraud_rate']})")
        print(f"Max PSI         : {report['max_psi']}")
        print(f"Drifted features: {report['drifted_features']}")
        print(f"Alerts          : {report['alerts']}")
    print("LIVE VARIATION: pass `--concept-drift` to inspect output shift.")


if __name__ == "__main__":
    main()
