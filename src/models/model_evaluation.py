from __future__ import annotations
import pandas as pd
from src import config

def write_model_metrics_table(forecast_metrics: dict, risk_metrics: dict) -> pd.DataFrame:
    rows = [{
        "model_name": forecast_metrics.get("model_name"),
        "model_type": forecast_metrics.get("model_type"),
        "target": forecast_metrics.get("target"),
        "mae": forecast_metrics.get("mae"),
        "rmse": forecast_metrics.get("rmse"),
        "mape": None, "accuracy": None, "precision": None, "recall": None, "f1": None, "roc_auc": None,
        "notes": forecast_metrics.get("notes"),
    }]
    for name, m in risk_metrics.items():
        rows.append({"model_name": name, "model_type": "classifier", "target": "high realization label", "mae": None, "rmse": None, "mape": None, "accuracy": m.get("accuracy"), "precision": m.get("precision"), "recall": m.get("recall"), "f1": m.get("f1"), "roc_auc": m.get("roc_auc"), "notes": m.get("notes")})
    df = pd.DataFrame(rows)
    df.to_csv(config.PROCESSED / "model_metrics.csv", index=False)
    return df
