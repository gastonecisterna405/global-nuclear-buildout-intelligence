from __future__ import annotations

import pandas as pd
import plotly.express as px
import streamlit as st
from src.dashboard.page_renderers._methodology import section as _method

from src import config


def render(forecasts: pd.DataFrame, metrics: pd.DataFrame) -> None:
    st.subheader("Capacity Forecasting — 2035")
    st.caption(
        "Model target is a scenario-derived heuristic (not historical ground truth). "
        "Metrics measure fit to the formula, not real-world predictive accuracy."
    )

    if forecasts.empty:
        st.warning("No forecast data. Run `python run_pipeline.py`.")
        return

    # Main forecast chart
    fc = forecasts.copy()
    fc["Forecast 2035 (GWe)"] = fc["forecast_capacity_2035_mwe"] / 1000
    fc["Heuristic target (GWe)"] = fc["target_capacity_2035_mwe"] / 1000
    fc = fc.sort_values("Forecast 2035 (GWe)", ascending=False)

    fig = px.bar(
        fc, x="country", y="Forecast 2035 (GWe)",
        color="region",
        hover_data={"Heuristic target (GWe)": True, "policy_signal_score": True},
        labels={"country": "Country", "region": "Region"},
        template="plotly_white",
    )
    fig.update_layout(
        margin=dict(t=10),
        xaxis=dict(title="", tickangle=-35),
        yaxis=dict(title="Forecast capacity 2035 (GWe)"),
        legend=dict(title="Region"),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Global trend
    trend_path = config.PREDICTIONS / "statsmodels_global_capacity_forecast.csv"
    if trend_path.exists():
        trend = pd.read_csv(trend_path)
        st.markdown("**Global capacity trend — Exponential Smoothing (Holt-Winters)**")
        fig2 = px.line(
            trend, x="year", y="global_capacity_mwe_forecast",
            labels={"year": "Year",
                    "global_capacity_mwe_forecast": "Global capacity (MWe)"},
            template="plotly_white",
            markers=True,
        )
        fig2.update_layout(margin=dict(t=10))
        st.plotly_chart(fig2, use_container_width=True)

    # Model metrics
    st.markdown("**Model evaluation metrics**")
    if not metrics.empty:
        show = metrics.dropna(axis=1, how="all")
        st.dataframe(show, use_container_width=True, hide_index=True)

    st.download_button(
        "⬇️  Download forecast CSV",
        forecasts.to_csv(index=False),
        "capacity_forecasts.csv",
        mime="text/csv",
    )
    _method(
        data="country_nuclear_profile.csv (34 country profiles with fleet stats and economic context)",
        features="operating/construction/planned/proposed capacity · GDP · population · electricity generation · nuclear share % · average fleet age · nuclear experience years · policy signal score (13 features total)",
        model="XGBoost Regressor (n_estimators=80, max_depth=3, lr=0.08) for cross-sectional country forecast · Holt-Winters Exponential Smoothing for global capacity trend extrapolation",
        notes="XGBoost target is a scenario heuristic (not historical ground truth) — metrics measure fit to the formula, not real-world accuracy. A production model requires timestamped PRIS snapshots."
    )
