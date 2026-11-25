"""Production monitoring, PSI/KS drift detection, and alert threshold management."""
from collections import deque
import math
from typing import Any

import numpy as np
from scipy import stats


def compute_psi(expected_pct: list[float], edges: list[float], actual_values: list[float]) -> float:
    """Population Stability Index between training bin proportions and live values."""
    if not actual_values or len(edges) < 2:
        return 0.0
    hist, _ = np.histogram(np.asarray(actual_values, dtype=float), bins=np.asarray(edges, dtype=float))
    total = max(int(hist.sum()), 1)
    psi = 0.0
    for exp_p, act_count in zip(expected_pct, hist):
        act_p = max(act_count / total, 1e-4)
        exp_p_safe = max(float(exp_p), 1e-4)
        psi += (act_p - exp_p_safe) * math.log(act_p / exp_p_safe)
    return round(float(psi), 4)


class DriftMonitor:
    """In-memory sliding-window monitor for inputs, predictions, latency, errors, and drift."""

    def __init__(
        self,
        reference_stats: dict[str, Any],
        window_size: int = 300,
        psi_warn: float = 0.15,
        psi_alert: float = 0.25,
        ks_alpha: float = 0.01,
    ) -> None:
        self.reference_stats = reference_stats
        self.window_size = window_size
        self.psi_warn = psi_warn
        self.psi_alert = psi_alert
        self.ks_alpha = ks_alpha

        self.feature_windows: dict[str, deque[float]] = {
            name: deque(maxlen=window_size) for name in reference_stats.get("features", {})
        }
        self.probs: deque[float] = deque(maxlen=window_size)
        self.preds: deque[int] = deque(maxlen=window_size)
        self.latencies_ms: deque[float] = deque(maxlen=window_size)
        self.total_requests = 0
        self.total_errors = 0

    def record_prediction(self, raw_input: dict[str, float], prob: float, pred: int, latency_ms: float) -> None:
        self.total_requests += 1
        for k, window in self.feature_windows.items():
            if k in raw_input:
                window.append(float(raw_input[k]))
        self.probs.append(float(prob))
        self.preds.append(int(pred))
        self.latencies_ms.append(float(latency_ms))

    def record_error(self) -> None:
        self.total_requests += 1
        self.total_errors += 1

    def reset(self) -> None:
        for w in self.feature_windows.values():
            w.clear()
        self.probs.clear()
        self.preds.clear()
        self.latencies_ms.clear()
        self.total_requests = 0
        self.total_errors = 0

    def summary(self) -> dict[str, Any]:
        """Compute per-feature PSI/KS drift, latency quantiles, prediction rate, and active alerts."""
        ref_features = self.reference_stats.get("features", {})
        feature_report: dict[str, dict[str, Any]] = {}
        drifted_features: list[str] = []
        max_psi = 0.0

        for name, ref in ref_features.items():
            vals = list(self.feature_windows.get(name, []))
            if len(vals) < 10:
                feature_report[name] = {"count": len(vals), "psi": 0.0, "ks_pvalue": 1.0, "status": "INSUFFICIENT_DATA"}
                continue
            psi = compute_psi(ref["expected_pct"], ref["edges"], vals)
            _, ks_p = stats.ks_2samp(ref["sample"], vals)
            max_psi = max(max_psi, psi)
            if psi >= self.psi_alert or (psi >= self.psi_warn and ks_p < self.ks_alpha):
                status = "DRIFT_ALERT"
                drifted_features.append(name)
            elif psi >= self.psi_warn:
                status = "WARN"
            else:
                status = "OK"
            feature_report[name] = {
                "count": len(vals),
                "mean_live": round(float(np.mean(vals)), 4),
                "mean_ref": round(float(ref["mean"]), 4),
                "psi": psi,
                "ks_pvalue": round(float(ks_p), 6),
                "status": status,
            }

        lat_arr = np.asarray(list(self.latencies_ms), dtype=float)
        p95_ms = round(float(np.percentile(lat_arr, 95)), 2) if len(lat_arr) else 0.0
        p50_ms = round(float(np.percentile(lat_arr, 50)), 2) if len(lat_arr) else 0.0
        live_fraud_rate = round(float(np.mean(self.preds)), 4) if self.preds else 0.0
        error_rate = round(self.total_errors / max(self.total_requests, 1), 4)

        alerts: list[str] = []
        if drifted_features:
            alerts.append(f"DATA_DRIFT detected on {drifted_features} (max_psi={max_psi})")
        if p95_ms > 200.0:
            alerts.append(f"HIGH_LATENCY p95={p95_ms}ms > 200ms")
        if error_rate > 0.05 and self.total_requests >= 10:
            alerts.append(f"HIGH_ERROR_RATE {error_rate * 100:.1f}%")

        return {
            "window_samples": len(self.preds),
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "error_rate": error_rate,
            "latency_p50_ms": p50_ms,
            "latency_p95_ms": p95_ms,
            "live_fraud_rate": live_fraud_rate,
            "ref_fraud_rate": round(float(self.reference_stats.get("fraud_rate", 0.0)), 4),
            "max_psi": max_psi,
            "drifted_features": drifted_features,
            "alerts": alerts,
            "overall_status": "ALERT" if alerts else "HEALTHY",
            "features": feature_report,
        }
