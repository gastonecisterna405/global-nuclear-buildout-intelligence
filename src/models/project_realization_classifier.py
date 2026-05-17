from __future__ import annotations
import json
import numpy as np
import pandas as pd
from joblib import dump
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
try:
    from xgboost import XGBClassifier
except Exception:
    XGBClassifier = None
from src import config

def train_project_realization_models(pipeline_df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    df = pipeline_df.copy()
    df["label_high_realization"] = (df["realization_probability"] >= 0.6).astype(int)
    features = ["status_group","technology_family","reactor_type","capacity_mwe","project_maturity_score","delay_risk_score"]
    X, y = df[features], df["label_high_realization"]
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["status_group","technology_family","reactor_type"]), ("num", StandardScaler(), ["capacity_mwe","project_maturity_score","delay_risk_score"])])
    candidates = {
        "logistic_regression": LogisticRegression(max_iter=1000),
        "random_forest": RandomForestClassifier(n_estimators=120, random_state=42),
    }
    if XGBClassifier:
        candidates["xgboost_classifier"] = XGBClassifier(n_estimators=60, max_depth=3, learning_rate=0.1, eval_metric="logloss", random_state=42)
    metrics = {}
    best_name, best_pipe, best_f1 = None, None, -1
    stratify = y if y.nunique() > 1 and y.value_counts().min() >= 2 else None
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.35, random_state=42, stratify=stratify) if len(df) >= 6 else (X, X, y, y)
    for name, model in candidates.items():
        pipe = Pipeline([("preprocess", pre), ("model", model)])
        pipe.fit(X_train, y_train)
        pred = pipe.predict(X_test)
        prob = pipe.predict_proba(X_test)[:, 1] if hasattr(pipe, "predict_proba") and y_test.nunique() > 1 else pred
        m = {
            "accuracy": float(accuracy_score(y_test, pred)),
            "precision": float(precision_score(y_test, pred, zero_division=0)),
            "recall": float(recall_score(y_test, pred, zero_division=0)),
            "f1": float(f1_score(y_test, pred, zero_division=0)),
            "roc_auc": float(roc_auc_score(y_test, prob)) if y_test.nunique() > 1 else None,
            "notes": "Labels are derived from transparent heuristic scoring because public historical realization labels are insufficient in the sample build.",
        }
        metrics[name] = m
        if m["f1"] > best_f1:
            best_name, best_pipe, best_f1 = name, pipe, m["f1"]
    df["risk_level"] = pd.cut(df["delay_risk_score"], bins=[0, 35, 65, 100], labels=["Low", "Medium", "High"], include_lowest=True).astype(str)
    df["realization_label"] = pd.cut(df["realization_probability"], bins=[0, 0.4, 0.7, 1], labels=["Low", "Medium", "High"], include_lowest=True).astype(str)
    out = df[["project_id","reactor_name","country","technology_family","capacity_mwe","delay_risk_score","risk_level","realization_probability","realization_label","project_maturity_score"]]
    out.to_csv(config.PREDICTIONS / "project_risk_scores.csv", index=False)
    (config.METRICS / "risk_model_metrics.json").write_text(json.dumps({"best_model": best_name, "models": metrics}, indent=2), encoding="utf-8")
    dump(best_pipe, config.MODELS / "project_realization_classifier.joblib")
    dump(best_pipe, config.MODELS / "delay_risk_model.joblib")
    return out, metrics
