from __future__ import annotations
import json
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from src import config

def score_technology_maturity(taxonomy: pd.DataFrame):
    df = taxonomy.copy()
    df["maturity_label"] = pd.cut(df["maturity_score"], bins=[0,30,55,75,100], labels=["Early", "Demonstration", "Commercializing", "Commercial"], include_lowest=True).astype(str)
    df["technology_risk_label"] = pd.cut(100 - df["maturity_score"], bins=[0,25,50,75,100], labels=["Low", "Medium", "High", "Very High"], include_lowest=True).astype(str)
    df["explanation"] = df.apply(lambda r: f"{r.reactor_type}: {r.deployment_status}; maturity reflects deployment, novelty, regulatory familiarity and sample pipeline counts.", axis=1)
    out = df[["technology_family","reactor_type","maturity_score","maturity_label","technology_risk_label","explanation"]]
    out.to_csv(config.PREDICTIONS / "technology_maturity_scores.csv", index=False)
    summary = {"average_maturity_score": float(df["maturity_score"].mean()), "lowest_maturity": df.sort_values("maturity_score").head(3)["reactor_type"].tolist(), "highest_maturity": df.sort_values("maturity_score", ascending=False).head(3)["reactor_type"].tolist()}
    (config.METRICS / "technology_maturity_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    pre = ColumnTransformer([("cat", OneHotEncoder(handle_unknown="ignore"), ["technology_family","reactor_type","coolant","moderator","deployment_status"])], remainder="passthrough")
    features = ["technology_family","reactor_type","coolant","moderator","deployment_status","smr_flag","geniv_flag","known_operating_units","known_under_construction_units"]
    model = Pipeline([("preprocess", pre), ("model", RandomForestRegressor(n_estimators=80, random_state=42))])
    model.fit(df[features], df["maturity_score"])
    dump(model, config.MODELS / "technology_maturity_model.joblib")
    return out, summary
