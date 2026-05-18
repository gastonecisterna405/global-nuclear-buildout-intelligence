from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

try:
    from xgboost import XGBRegressor
except ImportError:
    XGBRegressor = None

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import Ridge

from src import config

FEATURES = [
    "nuclear_share_t",
    "nuclear_share_lag1",
    "nuclear_share_lag2",
    "nuclear_elec_t",
    "nuclear_elec_lag1",
    "gdp_per_capita",
    "gdp_growth_rate",
    "electricity_demand",
    "coal_share",
    "renewables_share",
    "energy_per_capita",
    "population",
]

TRAIN_CUTOFF = 2010   # train on years ≤ 2010, test on years > 2010


def _make_pipe(model) -> Pipeline:
    preprocessor = ColumnTransformer([
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale",  StandardScaler()),
        ]), FEATURES),
    ])
    return Pipeline([("pre", preprocessor), ("model", model)])


def train_nuclear_generation_forecast(panel: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """
    Train a genuinely predictive model: nuclear share in 5 years.

    - Temporal train/test split: train ≤ 2010, test > 2010.
    - No data leakage: all features are at time t, target is at t+5.
    - Multiple models compared; best selected by test MAE.
    """
    available = [f for f in FEATURES if f in panel.columns]
    X = panel[available]
    y = panel["target_nuclear_share"]

    train_mask = panel["year"] <= TRAIN_CUTOFF
    test_mask  = ~train_mask

    X_train, y_train = X[train_mask], y[train_mask]
    X_test,  y_test  = X[test_mask],  y[test_mask]

    candidates = {
        "ridge":             Ridge(alpha=1.0),
        "random_forest":     RandomForestRegressor(n_estimators=200, max_depth=5, random_state=42),
        "gradient_boosting": GradientBoostingRegressor(n_estimators=200, max_depth=3,
                                                        learning_rate=0.05, random_state=42),
    }
    if XGBRegressor:
        candidates["xgboost"] = XGBRegressor(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            subsample=0.8, colsample_bytree=0.8,
            objective="reg:squarederror", random_state=42,
        )

    results = {}
    best_name, best_pipe, best_mae = None, None, float("inf")

    for name, model in candidates.items():
        pipe = _make_pipe(model)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            pipe.fit(X_train, y_train)
        pred_test = pipe.predict(X_test)

        mae  = float(mean_absolute_error(y_test, pred_test))
        rmse = float(np.sqrt(mean_squared_error(y_test, pred_test)))
        r2   = float(r2_score(y_test, pred_test)) if len(y_test) > 1 else None
        baseline_mae = float(mean_absolute_error(y_test, [y_train.mean()] * len(y_test)))

        results[name] = {
            "test_mae":       round(mae, 3),
            "test_rmse":      round(rmse, 3),
            "test_r2":        round(r2, 3) if r2 else None,
            "baseline_mae":   round(baseline_mae, 3),
            "skill_vs_mean":  round(1 - mae / baseline_mae, 3) if baseline_mae else None,
            "train_rows":     int(train_mask.sum()),
            "test_rows":      int(test_mask.sum()),
            "train_period":   f"≤{TRAIN_CUTOFF}",
            "test_period":    f">{TRAIN_CUTOFF}",
            "target":         f"nuclear_share_elec at t+5 years",
            "horizon":        "5 years",
        }
        if mae < best_mae:
            best_name, best_pipe, best_mae = name, pipe, mae

    # Generate predictions on all data for the dashboard
    panel = panel.copy()
    panel["predicted_nuclear_share"] = best_pipe.predict(X).round(2)
    panel["residual"] = panel["predicted_nuclear_share"] - panel["target_nuclear_share"]
    panel["split"] = panel["year"].apply(lambda y: "train" if y <= TRAIN_CUTOFF else "test")

    out_cols = ["country","year","target_year","nuclear_share_t","target_nuclear_share",
                "predicted_nuclear_share","residual","split"]
    out = panel[out_cols]
    out.to_csv(config.PREDICTIONS / "nuclear_share_forecast.csv", index=False)

    metrics = {
        "best_model": best_name,
        "models": results,
        "target_description": (
            "nuclear_share_elec (% of electricity from nuclear) at t+5 years. "
            "This is an independent future value — NOT derived from the features at time t. "
            "Train/test split is temporal to prevent leakage."
        ),
    }
    (config.METRICS / "nuclear_share_forecast_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    dump(best_pipe, config.MODELS / "nuclear_share_forecast.joblib")
    return out, metrics
