from __future__ import annotations

import json
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
try:
    from xgboost import XGBRegressor
except Exception:
    XGBRegressor = None
from sklearn.ensemble import RandomForestRegressor
from src import config

def train_capacity_forecaster(countries: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = countries.copy()
    df["target_capacity_2035_mwe"] = df["operating_capacity_mwe"] + 0.75 * df["construction_capacity_mwe"] + 0.45 * df["planned_capacity_mwe"] + 0.15 * df["proposed_capacity_mwe"]
    features = ["region","income_group","gdp_current_usd","population","electricity_generation_twh","nuclear_share_percent","operating_capacity_mwe","construction_capacity_mwe","planned_capacity_mwe","proposed_capacity_mwe","average_fleet_age","nuclear_experience_years","policy_signal_score"]
    X, y = df[features], df["target_capacity_2035_mwe"]
    numeric = [c for c in features if c not in ["region","income_group"]]
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["region","income_group"]), ("num", StandardScaler(), numeric)])
    model = XGBRegressor(n_estimators=80, max_depth=3, learning_rate=0.08, objective="reg:squarederror", random_state=42) if XGBRegressor else RandomForestRegressor(n_estimators=120, random_state=42)
    pipe = Pipeline([("preprocess", pre), ("model", model)])
    if len(df) >= 8:
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42)
    else:
        X_train, X_test, y_train, y_test = X, X, y, y
    pipe.fit(X_train, y_train)
    pred = pipe.predict(X_test)
    metrics = {
        "model_name": "capacity_forecast_xgboost_or_rf",
        "model_type": "XGBoostRegressor" if XGBRegressor else "RandomForestRegressor fallback",
        "target": "heuristic expected capacity by 2035 from current fleet and pipeline",
        "mae": float(mean_absolute_error(y_test, pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, pred))),
        "r2": float(r2_score(y_test, pred)) if len(y_test) > 1 else None,
        "notes": "Portfolio sample target is scenario-derived. Replace with historical snapshots for production validation.",
    }
    df["forecast_capacity_2035_mwe"] = pipe.predict(X).round(1)
    out = df[["country","region","forecast_capacity_2035_mwe","target_capacity_2035_mwe","policy_signal_score"]]
    out.to_csv(config.PREDICTIONS / "capacity_forecasts.csv", index=False)
    (config.METRICS / "forecasting_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    dump(pipe, config.MODELS / "capacity_forecast_xgboost.joblib")
    return out, metrics
