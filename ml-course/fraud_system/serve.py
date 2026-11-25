"""FastAPI serving service for the Fraud Detection model (Wed + Thu + Fri).

Endpoints:
  GET  /health            liveness + active model version
  POST /v1/predict        validated real-time fraud scoring
  GET  /v1/model-info     active model params, metrics, and rollback history
  POST /v1/rollback       switch back to baseline model or custom threshold
  GET  /v1/monitor/drift  live PSI / KS drift report + latency & alert status
  POST /v1/monitor/simulate  generate clean or drifted live transactions for demoing
  POST /v1/monitor/reset  clear monitoring sliding window
  GET  /metrics           Prometheus-compatible metrics exposition
"""
from contextlib import asynccontextmanager
import json
import os
from pathlib import Path
import time
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from .data_gen import generate_transactions
from .features import engineer_features
from .monitor import DriftMonitor
from .train import train_and_save

ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))
DATA_PATH = Path(os.getenv("DATA_PATH", "data/transactions.csv"))
PARAMS_PATH = Path(os.getenv("PARAMS_PATH", "params.yaml"))
WEB_INDEX = Path(__file__).resolve().parent.parent / "web" / "index.html"
FAULT_STATE = Path(os.getenv("FAULT_STATE_PATH", ".fault_state.json"))


class TransactionIn(BaseModel):
    amount: float = Field(gt=0, le=1_000_000, description="Transaction amount in USD")
    hour_of_day: int = Field(ge=0, le=23, description="Hour of day (0-23)")
    merchant_risk_score: float = Field(ge=0.0, le=1.0, description="Merchant risk score [0, 1]")
    tx_velocity_24h: int = Field(ge=1, le=500, description="Transactions by card in last 24h")
    distance_from_home_km: float = Field(ge=0.0, le=25_000.0, description="Distance from cardholder home")
    is_international: Literal[0, 1] = Field(description="1 if cross-border, else 0")
    card_present: Literal[0, 1] = Field(description="1 if physical card present, else 0")
    account_age_days: int = Field(ge=1, le=40_000, description="Age of account in days")


class PredictionOut(BaseModel):
    is_fraud: bool
    fraud_probability: float
    threshold: float
    risk_band: str
    model_version: str
    latency_ms: float


class SimulateIn(BaseModel):
    n: int = Field(default=60, ge=10, le=500)
    data_drift: bool = False
    concept_drift: bool = False
    seed: int = 101


class RollbackIn(BaseModel):
    threshold: float | None = Field(default=None, gt=0.0, lt=1.0)
    restore_baseline: bool = True


_state: dict = {}


def _load_bundle_and_monitor() -> None:
    model_path = ARTIFACTS_DIR / "model.joblib"
    ref_path = ARTIFACTS_DIR / "reference_stats.json"
    if not model_path.exists() or not ref_path.exists():
        train_and_save(data_path=DATA_PATH, params_path=PARAMS_PATH, artifacts_dir=ARTIFACTS_DIR)
    bundle = joblib.load(model_path)
    ref_stats = json.loads(ref_path.read_text(encoding="utf-8"))
    _state["bundle"] = bundle
    _state["baseline_bundle"] = dict(bundle)
    _state["monitor"] = DriftMonitor(ref_stats)


def _active_fault() -> dict:
    if FAULT_STATE.exists():
        try:
            return json.loads(FAULT_STATE.read_text(encoding="utf-8-sig"))
        except Exception:
            return {}
    return {}


@asynccontextmanager
async def lifespan(_app: FastAPI):
    _load_bundle_and_monitor()
    yield


app = FastAPI(title="Fraud Detection MLOps API", version="1.0.0", lifespan=lifespan)


@app.exception_handler(Exception)
async def _unhandled_exception(_request: Request, exc: Exception):
    if "monitor" in _state:
        _state["monitor"].record_error()
    return JSONResponse(status_code=500, content={"detail": f"Internal prediction error: {type(exc).__name__}"})


@app.get("/", response_class=HTMLResponse)
def dashboard():
    if WEB_INDEX.exists():
        return HTMLResponse(WEB_INDEX.read_text(encoding="utf-8"))
    return HTMLResponse("<h1>Fraud Detection MLOps API</h1><p>Open <a href='/docs'>/docs</a></p>")


@app.get("/health")
def health():
    if "bundle" not in _state:
        _load_bundle_and_monitor()
    fault = _active_fault()
    if fault.get("fault") == "bad-schema":
        return JSONResponse(status_code=503, content={"status": "degraded", "reason": "fault injected: bad-schema"})
    return {"status": "ok", "model_version": _state["bundle"]["version"]}


@app.get("/v1/model-info")
def model_info():
    if "bundle" not in _state:
        _load_bundle_and_monitor()
    b = _state["bundle"]
    return {
        "model_version": b["version"],
        "threshold": b["threshold"],
        "params": b["params"],
        "metrics": b["metrics"],
        "features": b["features"],
    }


@app.post("/v1/predict", response_model=PredictionOut)
def predict(tx: TransactionIn):
    if "bundle" not in _state:
        _load_bundle_and_monitor()
    fault = _active_fault()
    t0 = time.perf_counter()
    if fault.get("fault") == "latency-spike":
        time.sleep(0.25)

    bundle = _state["bundle"]
    raw = tx.model_dump()
    if fault.get("fault") == "bad-schema":
        _state["monitor"].record_error()
        raise HTTPException(status_code=500, detail="Simulated schema mismatch: missing feature column 'log_amount'")

    X = engineer_features(pd.DataFrame([raw]))
    prob = float(bundle["pipeline"].predict_proba(X)[0, 1])
    threshold = float(bundle["threshold"])
    is_fraud = prob >= threshold
    latency_ms = round((time.perf_counter() - t0) * 1000.0, 2)

    _state["monitor"].record_prediction(raw, prob, int(is_fraud), latency_ms)
    band = "HIGH" if prob >= 0.7 else ("MEDIUM" if prob >= threshold else "LOW")
    return PredictionOut(
        is_fraud=is_fraud,
        fraud_probability=round(prob, 4),
        threshold=threshold,
        risk_band=band,
        model_version=bundle["version"],
        latency_ms=latency_ms,
    )


@app.post("/v1/rollback")
def rollback(req: RollbackIn):
    if "bundle" not in _state:
        _load_bundle_and_monitor()
    if req.restore_baseline:
        _state["bundle"] = dict(_state["baseline_bundle"])
    if req.threshold is not None:
        _state["bundle"]["threshold"] = float(req.threshold)
        _state["bundle"]["version"] = _state["baseline_bundle"]["version"] + f"-thr{req.threshold}"
    return {"status": "rolled_back", "active_version": _state["bundle"]["version"], "threshold": _state["bundle"]["threshold"]}


@app.get("/v1/monitor/drift")
def drift_report():
    if "monitor" not in _state:
        _load_bundle_and_monitor()
    return _state["monitor"].summary()


@app.post("/v1/monitor/simulate")
def simulate_stream(req: SimulateIn):
    if "bundle" not in _state:
        _load_bundle_and_monitor()
    df = generate_transactions(n_rows=req.n, seed=req.seed, data_drift=req.data_drift, concept_drift=req.concept_drift)
    bundle = _state["bundle"]
    X = engineer_features(df)
    probs = bundle["pipeline"].predict_proba(X)[:, 1]
    thr = float(bundle["threshold"])
    for row, prob in zip(df.to_dict(orient="records"), probs):
        _state["monitor"].record_prediction(row, float(prob), int(prob >= thr), latency_ms=4.5)
    return _state["monitor"].summary()


@app.post("/v1/monitor/reset")
def reset_monitor():
    if "monitor" in _state:
        _state["monitor"].reset()
    return {"status": "reset"}


@app.get("/metrics")
def prometheus_metrics():
    if "monitor" not in _state:
        _load_bundle_and_monitor()
    s = _state["monitor"].summary()
    lines = [
        "# HELP fraud_requests_total Total prediction requests",
        "# TYPE fraud_requests_total counter",
        f"fraud_requests_total {s['total_requests']}",
        "# HELP fraud_errors_total Total prediction errors",
        "# TYPE fraud_errors_total counter",
        f"fraud_errors_total {s['total_errors']}",
        "# HELP fraud_latency_p95_ms 95th percentile inference latency in ms",
        "# TYPE fraud_latency_p95_ms gauge",
        f"fraud_latency_p95_ms {s['latency_p95_ms']}",
        "# HELP fraud_max_psi Maximum Population Stability Index across monitored features",
        "# TYPE fraud_max_psi gauge",
        f"fraud_max_psi {s['max_psi']}",
        "# HELP fraud_live_rate Live predicted fraud rate",
        "# TYPE fraud_live_rate gauge",
        f"fraud_live_rate {s['live_fraud_rate']}",
    ]
    return Response("\n".join(lines) + "\n", media_type="text/plain; version=0.0.4")
