from __future__ import annotations
import json
import pandas as pd
from joblib import dump
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from src import config

CLUSTER_NAMES = {
    0: "Mature or legacy fleet",
    1: "High-growth builder",
    2: "Emerging nuclear entrant",
    3: "Advanced technology explorer",
}

def cluster_countries(countries: pd.DataFrame):
    features = ["operating_capacity_mwe","construction_capacity_mwe","planned_capacity_mwe","proposed_capacity_mwe","nuclear_share_percent","gdp_current_usd","electricity_generation_twh","population","average_fleet_age","advanced_reactor_activity_score","policy_signal_score"]
    X = countries[features].fillna(0)
    n = min(4, max(2, len(countries) // 4))
    pipe = Pipeline([("scale", StandardScaler()), ("kmeans", KMeans(n_clusters=n, random_state=42, n_init=10))])
    labels = pipe.fit_predict(X)
    coords = PCA(n_components=2, random_state=42).fit_transform(StandardScaler().fit_transform(X))
    out = countries[["country","region"]].copy()
    out["cluster_id"] = labels
    out["cluster_name"] = out["cluster_id"].map(CLUSTER_NAMES).fillna("Nuclear strategy segment")
    out["pca_x"], out["pca_y"] = coords[:,0], coords[:,1]
    out.to_csv(config.PREDICTIONS / "country_clusters.csv", index=False)
    metrics = {"n_clusters": int(n), "silhouette_score": float(silhouette_score(StandardScaler().fit_transform(X), labels)) if n > 1 and len(set(labels)) > 1 else None}
    (config.METRICS / "clustering_metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    dump(pipe, config.MODELS / "country_clustering_model.joblib")
    return out, metrics
