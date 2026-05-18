from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src import config
from src.dashboard.page_renderers._methodology import section as _method


def _load_real_model_results():
    pred_path    = config.PREDICTIONS / "nuclear_share_forecast.csv"
    metrics_path = config.METRICS / "nuclear_share_forecast_metrics.json"
    if pred_path.exists() and metrics_path.exists():
        return pd.read_csv(pred_path), json.loads(metrics_path.read_text())
    return None, None


def render(forecasts: pd.DataFrame, metrics: pd.DataFrame) -> None:
    st.subheader("Forecasting — Nuclear Share & Capacity")

    panel_preds, panel_metrics = _load_real_model_results()
    has_real_model = panel_preds is not None

    # ── REAL MODEL ─────────────────────────────────────────────────────────────
    if has_real_model:
        st.success(
            "Real predictive model trained on OWID panel data "
            f"({panel_preds.country.nunique()} countries, "
            f"{panel_preds.year.min()}–{panel_preds.year.max()})."
        )

        best_name = panel_metrics["best_model"]
        best      = panel_metrics["models"][best_name]

        cols = st.columns(5)
        cols[0].metric("Model",               best_name.replace("_"," ").title())
        cols[1].metric("Test MAE",             f"{best['test_mae']:.2f} pp")
        cols[2].metric("Test R²",              f"{best['test_r2']:.3f}")
        cols[3].metric("Skill vs mean",        f"{best['skill_vs_mean']:.1%}")
        cols[4].metric("Test rows",            best["test_rows"])

        st.caption(
            f"Train period: {best['train_period']} · Test period: {best['test_period']} · "
            "Target: nuclear share of electricity 5 years ahead. "
            "**Temporal split — no data leakage.**"
        )

        st.divider()

        # Model comparison
        st.markdown("#### Model comparison (test set)")
        comp_rows = []
        for name, m in panel_metrics["models"].items():
            comp_rows.append({
                "Model": name.replace("_"," ").title(),
                "Test MAE (pp)": m["test_mae"],
                "Test R²": m.get("test_r2",""),
                "Skill vs mean": m.get("skill_vs_mean",""),
                "Train rows": m["train_rows"],
                "Test rows":  m["test_rows"],
            })
        st.dataframe(pd.DataFrame(comp_rows), use_container_width=True, hide_index=True)

        st.divider()

        # Predicted vs actual scatter (test set)
        st.markdown("#### Predicted vs Actual nuclear share — test set (post-2010)")
        test = panel_preds[panel_preds.split == "test"].copy()

        fig = px.scatter(
            test,
            x="target_nuclear_share",
            y="predicted_nuclear_share",
            color="country",
            hover_data=["year", "target_year"],
            labels={
                "target_nuclear_share":    "Actual nuclear share (%)",
                "predicted_nuclear_share": "Predicted nuclear share (%)",
            },
            template="plotly_white",
            opacity=0.7,
        )
        max_val = max(test.target_nuclear_share.max(), test.predicted_nuclear_share.max()) * 1.05
        fig.add_shape(type="line", x0=0, y0=0, x1=max_val, y1=max_val,
                      line=dict(color="gray", dash="dot", width=1.5))
        fig.update_layout(margin=dict(t=10), showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

        # Time series: selected country
        st.markdown("#### Country forecast trajectory")
        countries_available = sorted(panel_preds.country.unique())
        sel = st.selectbox("Select country", countries_available,
                           index=countries_available.index("France")
                           if "France" in countries_available else 0)

        cdf = panel_preds[panel_preds.country == sel].sort_values("year")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=cdf[cdf.split=="train"]["year"],
                                   y=cdf[cdf.split=="train"]["target_nuclear_share"],
                                   name="Actual (train)", mode="lines",
                                   line=dict(color="#2563eb")))
        fig2.add_trace(go.Scatter(x=cdf[cdf.split=="test"]["year"],
                                   y=cdf[cdf.split=="test"]["target_nuclear_share"],
                                   name="Actual (test)", mode="lines",
                                   line=dict(color="#2563eb", dash="dot")))
        fig2.add_trace(go.Scatter(x=cdf[cdf.split=="test"]["year"],
                                   y=cdf[cdf.split=="test"]["predicted_nuclear_share"],
                                   name="Predicted (test)", mode="lines+markers",
                                   line=dict(color="#ef4444")))
        fig2.add_vline(x=2010, line_dash="dash", line_color="gray",
                       annotation_text="Train / Test split")
        fig2.update_layout(template="plotly_white", margin=dict(t=10),
                            yaxis_title="Nuclear share (%)", xaxis_title="Year")
        st.plotly_chart(fig2, use_container_width=True)

        st.divider()

    else:
        st.warning(
            "Real panel model not available — OWID data was not downloaded. "
            "Run `python run_pipeline.py` with internet access to train the predictive model."
        )

    # ── DEMO MODELS (for context) ──────────────────────────────────────────────
    with st.expander("Legacy models — cross-sectional XGBoost (demo, circular target)"):
        st.caption(
            "This model predicts 2035 capacity from country-level features. "
            "The target is a heuristic formula — not historical ground truth. "
            "Metrics measure fit to the formula, not predictive accuracy."
        )
        if not forecasts.empty:
            fc = forecasts.copy()
            fc["Forecast 2035 (GWe)"] = fc["forecast_capacity_2035_mwe"] / 1000
            fc = fc.sort_values("Forecast 2035 (GWe)", ascending=False)
            fig3 = px.bar(fc, x="country", y="Forecast 2035 (GWe)",
                          color="region", template="plotly_white",
                          labels={"country":"Country","region":"Region"})
            fig3.update_layout(xaxis=dict(tickangle=-35), margin=dict(t=10))
            st.plotly_chart(fig3, use_container_width=True)

        trend_path = config.PREDICTIONS / "statsmodels_global_capacity_forecast.csv"
        if trend_path.exists():
            trend = pd.read_csv(trend_path)
            fig4 = px.line(trend, x="year", y="global_capacity_mwe_forecast",
                           template="plotly_white", markers=True,
                           labels={"year":"Year",
                                   "global_capacity_mwe_forecast":"Global capacity (MWe)"})
            fig4.update_layout(margin=dict(t=10))
            st.plotly_chart(fig4, use_container_width=True)

        if not metrics.empty:
            st.dataframe(metrics.dropna(axis=1, how="all"),
                         use_container_width=True, hide_index=True)

    st.download_button(
        "Download predictions CSV",
        panel_preds.to_csv(index=False) if has_real_model else forecasts.to_csv(index=False),
        "nuclear_forecast.csv",
        mime="text/csv",
    )

    _method(
        data="OWID energy data — 1,656 country-year observations, 47 countries, 1975–2020 "
             "(downloaded from github.com/owid/energy-data)",
        features="nuclear_share_t · nuclear_share_lag1 · nuclear_share_lag2 · "
                 "nuclear_elec_t · nuclear_elec_lag1 · gdp_per_capita · "
                 "gdp_growth_rate · electricity_demand · coal_share · renewables_share · "
                 "energy_per_capita · population (12 features)",
        model="Gradient Boosting Regressor (best) vs Ridge / RF / XGBoost. "
              "Train ≤ 2010, Test > 2010 — temporal split, no leakage. "
              f"Target: nuclear_share_elec at t+5 years (independent future value).",
        notes="This is a genuinely predictive model. "
              "R²=0.92 and Skill=0.81 on held-out test data (post-2010). "
              "Contrast with the legacy XGBoost model whose target is circular.",
    )
