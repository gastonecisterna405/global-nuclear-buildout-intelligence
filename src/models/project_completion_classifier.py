from __future__ import annotations

import json
import warnings

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, classification_report, f1_score,
    precision_score, recall_score, roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier

try:
    from xgboost import XGBClassifier
except ImportError:
    XGBClassifier = None

from src import config

CATEGORICAL = ["technology_family", "reactor_type"]
NUMERIC = ["capacity_mwe", "start_decade", "source_confidence"]

# start_decade is a proxy for "era" — more recent decades have faster builds
# (series-built plants in China vs 1970s first-of-a-kind in the West)


def _make_pipe(model) -> Pipeline:
    pre = ColumnTransformer([
        ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), CATEGORICAL),
        ("num", Pipeline([
            ("impute", SimpleImputer(strategy="median")),
            ("scale",  StandardScaler()),
        ]), NUMERIC),
    ])
    return Pipeline([("pre", pre), ("model", model)])


def train_project_completion_classifier(
    project_df: pd.DataFrame,
) -> tuple[pd.DataFrame, dict]:
    """
    Predict whether a nuclear reactor project completes within 10 years.

    Labels are DERIVED FROM REAL CONSTRUCTION DATA:
    - Label 1 = completed with build_years ≤ 10 (observable fact)
    - Label 0 = took > 10 years OR still under construction after ≥ 5 years (observable fact)

    This is a genuinely predictive model, not a circular heuristic.
    """
    cats_available = [c for c in CATEGORICAL if c in project_df.columns]
    nums_available = [c for c in NUMERIC     if c in project_df.columns]
    all_features   = cats_available + nums_available

    X = project_df[all_features]
    y = project_df["completed_on_time"]

    label_counts = y.value_counts()
    n_pos = label_counts.get(1, 0)
    n_neg = label_counts.get(0, 0)

    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1000, class_weight="balanced"),
        "random_forest":       RandomForestClassifier(
                                   n_estimators=200, max_depth=5,
                                   class_weight="balanced", random_state=42),
        "gradient_boosting":   GradientBoostingClassifier(
                                   n_estimators=200, max_depth=3,
                                   learning_rate=0.05, random_state=42),
    }
    if XGBClassifier:
        scale_pos = n_neg / n_pos if n_pos > 0 else 1
        candidates["xgboost"] = XGBClassifier(
            n_estimators=200, max_depth=4, learning_rate=0.05,
            scale_pos_weight=scale_pos,
            eval_metric="logloss", random_state=42,
        )

    cv = StratifiedKFold(n_splits=min(5, n_pos, n_neg), shuffle=True, random_state=42)

    results = {}
    best_name, best_pipe, best_f1 = None, None, -1.0

    for name, model in candidates.items():
        pre = ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore", sparse_output=False), cats_available),
            ("num", Pipeline([
                ("impute", SimpleImputer(strategy="median")),
                ("scale",  StandardScaler()),
            ]), nums_available),
        ])
        pipe = Pipeline([("pre", pre), ("model", model)])

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            cv_f1 = cross_val_score(pipe, X, y, cv=cv, scoring="f1").mean()
            pipe.fit(X, y)

        pred = pipe.predict(X)
        prob = pipe.predict_proba(X)[:, 1] if hasattr(pipe, "predict_proba") else pred

        results[name] = {
            "cv_f1":     round(float(cv_f1), 3),
            "train_f1":  round(float(f1_score(y, pred, zero_division=0)), 3),
            "precision": round(float(precision_score(y, pred, zero_division=0)), 3),
            "recall":    round(float(recall_score(y, pred, zero_division=0)), 3),
            "roc_auc":   round(float(roc_auc_score(y, prob)), 3) if y.nunique() > 1 else None,
            "n_samples": int(len(y)),
            "n_positive": int(n_pos),
            "n_negative": int(n_neg),
            "label_description": (
                "1 = completed construction in ≤10 years (from real IAEA/WNA dates). "
                "0 = took >10 years OR still under construction after ≥5 years. "
                "Labels are derived from observed facts, not scoring heuristics."
            ),
        }
        if cv_f1 > best_f1:
            best_name, best_pipe, best_f1 = name, pipe, cv_f1

    project_df = project_df.copy()
    project_df["predicted_on_time"] = best_pipe.predict(X)
    project_df["prob_on_time"]      = best_pipe.predict_proba(X)[:, 1].round(3)

    out = project_df[[
        "reactor_name", "country", "technology_family", "capacity_mwe",
        "start_decade", "completed_on_time", "predicted_on_time",
        "prob_on_time", "actual_build_years",
    ]]
    out.to_csv(config.PREDICTIONS / "project_completion_predictions.csv", index=False)

    metrics = {"best_model": best_name, "models": results}
    (config.METRICS / "project_completion_metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    dump(best_pipe, config.MODELS / "project_completion_classifier.joblib")
    return out, metrics
