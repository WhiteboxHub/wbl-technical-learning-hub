"""Shared feature engineering logic used identically in training and serving.

Keeping feature transformations in one module prevents training-serving skew.
"""
import numpy as np
import pandas as pd

RAW_FEATURES = [
    "amount",
    "hour_of_day",
    "merchant_risk_score",
    "tx_velocity_24h",
    "distance_from_home_km",
    "is_international",
    "card_present",
    "account_age_days",
]

ENGINEERED_FEATURES = RAW_FEATURES + [
    "log_amount",
    "amount_per_tx_24h",
    "is_night",
    "high_risk_intl",
]

TARGET_COL = "is_fraud"


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:
    """Compute deterministic derived features from raw transaction attributes."""
    out = df[RAW_FEATURES].copy()
    out["log_amount"] = np.log1p(np.maximum(out["amount"].astype(float), 0.0))
    out["amount_per_tx_24h"] = out["amount"].astype(float) / np.maximum(out["tx_velocity_24h"].astype(float), 1.0)
    out["is_night"] = ((out["hour_of_day"] < 6) | (out["hour_of_day"] >= 23)).astype(int)
    out["high_risk_intl"] = ((out["is_international"] == 1) & (out["merchant_risk_score"] >= 0.5)).astype(int)
    return out[ENGINEERED_FEATURES]


def prepare_xy(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return engineered feature matrix X and binary target series y."""
    X = engineer_features(df)
    y = df[TARGET_COL].astype(int)
    return X, y
