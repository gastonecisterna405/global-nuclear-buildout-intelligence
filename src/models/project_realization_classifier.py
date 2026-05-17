from __future__ import annotations

import json

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None

from src import config

FEATURES = [
    "status_group", "technology_family", "reactor_type",
    "capacity_mwe", "project_maturity_score", "delay_risk_score",
]
CATEGORICAL = ["status_group", "technology_family", "reactor_type"]
NUMERIC = ["capacity_mwe", "project_maturity_score", "delay_risk_score"]

# Label is derived from realization_probability which itself comes from project_maturity_score.
# With sample data there are no historical realization labels, so the model demonstrates the
# pipeline pattern rather than learning from independent outcomes.
_REALIZATION_THRESHOLD = 0.6


def _evaluate(pipe: Pipeline, X_test, y_test) -> dict:
    pred = pipe.predict(X_test)
    has_both_classes = y_test.nunique() > 1
    prob = pipe.predict_proba(X_test)[:, 1] if has_both_classes else pred
    return {
        "accuracy": float(accuracy_score(y_test, pred)),
        "precision": float(precision_score(y_test, pred, zero_division=0)),
        "recall": float(recall_score(y_test, pred, zero_division=0)),
        "f1": float(f1_score(y_test, pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, prob)) if has_both_classes else None,
        "notes": (
            "Labels are derived from heuristic scoring (no historical realization data). "
            "Metrics measure consistency with the scoring rule, not real-world predictive accuracy."
        ),
    }


def train_project_realization_models(pipeline_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = pipeline_df.copy()
    df["label_high_realization"] = (df["realization_probability"] >= _REALIZATION_THRESHOLD).astype(int)

    X, y = df[FEATURES], df["label_high_realization"]

    preprocessor = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL),
        ("num", StandardScaler(), NUMERIC),
    ])

    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
    }
    if XGBClassifier:
        candidates["xgboost_classifier"] = XGBClassifier(
            n_estimators=60, max_depth=3, learning_rate=0.1,
            eval_metric="logloss", random_state=42,
        )

    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
    if len(df) >= 6:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.35, random_state=42, stratify=stratify
        )
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    all_metrics: dict = {}
    best_name, best_pipe, best_f1 = None, None, -1.0

    for name, model in candidates.items():
        pipe = Pipeline([("preprocess", preprocessor), ("model", model)])
        pipe.fit(X_train, y_train)
        m = _evaluate(pipe, X_test, y_test)
        all_metrics[name] = m
        if m["f1"] > best_f1:
            best_name, best_pipe, best_f1 = name, pipe, m["f1"]

    df["risk_level"] = pd.cut(
        df["delay_risk_score"], bins=[0, 35, 65, 100],
        labels=["Low", "Medium", "High"], include_lowest=True,
    ).astype(str)
    df["realization_label"] = pd.cut(
        df["realization_probability"], bins=[0, 0.4, 0.7, 1.0],
        labels=["Low", "Medium", "High"], include_lowest=True,
    ).astype(str)

    out_cols = [
        "project_id", "reactor_name", "country", "technology_family",
        "capacity_mwe", "delay_risk_score", "risk_level",
        "realization_probability", "realization_label", "project_maturity_score",
    ]
    out = df[out_cols]
    out.to_csv(config.PREDICTIONS / "project_risk_scores.csv", index=False)
    (config.METRICS / "risk_model_metrics.json").write_text(
        json.dumps({"best_model": best_name, "models": all_metrics}, indent=2),
        encoding="utf-8",
    )
    dump(best_pipe, config.MODELS / "project_realization_classifier.joblib")
    dump(best_pipe, config.MODELS / "delay_risk_model.joblib")
    return out, all_metrics
