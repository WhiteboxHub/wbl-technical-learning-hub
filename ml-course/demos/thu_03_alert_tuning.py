"""Thursday Demo 3: Alert storm tuned from noisy (every tiny blip) to 3 actionable alerts.

Live variation: --mode noisy vs --mode tuned.
"""
import argparse


def evaluate_alerts(mode: str) -> list[str]:
    signals = [
        ("tx_amount_mean_shift", 0.06),
        ("hour_of_day_shift", 0.04),
        ("single_500ms_request", 1),
        ("merchant_risk_psi", 0.31),
        ("p95_latency_ms", 245.0),
        ("error_rate_pct", 7.2),
        ("card_present_psi", 0.07),
    ]
    if mode == "noisy":
        # Fires on every trivial fluctuation -> alarm fatigue
        return [f"ALERT: {k}={v}" for k, v in signals for _ in range(7)]
    # Tuned: only actionable conditions (PSI >= 0.25, p95 > 200ms, error_rate > 5%)
    fired = []
    for k, v in signals:
        if k == "merchant_risk_psi" and v >= 0.25:
            fired.append(f"ACTIONABLE [DRIFT]: {k}={v} >= 0.25 -> inspect feature pipeline / retrain")
        elif k == "p95_latency_ms" and v > 200:
            fired.append(f"ACTIONABLE [LATENCY]: {k}={v}ms > 200ms -> scale workers")
        elif k == "error_rate_pct" and v > 5.0:
            fired.append(f"ACTIONABLE [ERRORS]: {k}={v}% > 5% -> check input schema")
    return fired


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["noisy", "tuned"], default="noisy", help="Live variation: noisy vs tuned")
    args = parser.parse_args()

    print("\n=== THURSDAY DEMO 3: ALERT TUNING (NOISE VS SIGNAL) ===")
    alerts = evaluate_alerts(args.mode)
    print(f"Mode={args.mode.upper()} | Total alerts fired: {len(alerts)}")
    for line in alerts[:6]:
        print(" ", line)
    if len(alerts) > 6:
        print(f"  ... ({len(alerts) - 6} more noisy alerts suppressed from terminal)")
    print("LIVE VARIATION: re-run with `--mode tuned` to reduce 49 noisy alerts to 3 actionable alerts.")


if __name__ == "__main__":
    main()
