from __future__ import annotations

import json

import pandas as pd
import plotly.express as px
import streamlit as st

from src import config
from src.dashboard.page_renderers._methodology import section as _method

STATUS_COLORS = {
    "Construction": "#f59e0b",
    "Planned":      "#10b981",
    "Proposed":     "#8b5cf6",
}


def _load_completion_results():
    pred_path    = config.PREDICTIONS / "project_completion_predictions.csv"
    metrics_path = config.METRICS / "project_completion_metrics.json"
    if pred_path.exists() and metrics_path.exists():
        return pd.read_csv(pred_path), json.loads(metrics_path.read_text())
    return None, None


def render(risk: pd.DataFrame) -> None:
    st.subheader("Project Risk Scoring")

    comp_preds, comp_metrics = _load_completion_results()
    has_real = comp_preds is not None

    # ── REAL MODEL ─────────────────────────────────────────────────────────────
    if has_real:
        st.success(
            f"Real classifier trained on {len(comp_preds)} labeled nuclear projects "
            f"(completion derived from actual IAEA/WNA construction dates)."
        )

        best_name = comp_metrics["best_model"]
        best      = comp_metrics["models"][best_name]

        cols = st.columns(5)
        cols[0].metric("Model",       best_name.replace("_"," ").title())
        cols[1].metric("CV F1",       f"{best['cv_f1']:.3f}")
        cols[2].metric("ROC-AUC",     f"{best.get('roc_auc','?')}")
        cols[3].metric("On-time",     f"{best['n_positive']} projects")
        cols[4].metric("Delayed",     f"{best['n_negative']} projects")

        st.caption(
            "**Label = 1:** project completed construction in ≤10 years (observed fact). "
            "**Label = 0:** took >10 years OR still under construction after ≥5 years. "
            "These are real historical outcomes — not derived from a scoring formula."
        )

        st.divider()

        # Model comparison
        st.markdown("#### Model comparison (cross-validation)")
        rows = []
        for name, m in comp_metrics["models"].items():
            rows.append({
                "Model":      name.replace("_"," ").title(),
                "CV F1":      m["cv_f1"],
                "Precision":  m["precision"],
                "Recall":     m["recall"],
                "ROC-AUC":    m.get("roc_auc",""),
                "Samples":    m["n_samples"],
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.divider()

        # Build time distribution
        st.markdown("#### Actual construction duration by technology")
        valid = comp_preds.dropna(subset=["actual_build_years"])
        if not valid.empty:
            fig = px.box(
                valid, x="technology_family", y="actual_build_years",
                color="technology_family", template="plotly_white",
                points="all",
                labels={"technology_family":"Technology",
                        "actual_build_years":"Actual build time (years)"},
            )
            fig.add_hline(y=10, line_dash="dash", line_color="red",
                          annotation_text="10-year threshold")
            fig.update_layout(showlegend=False, margin=dict(t=10),
                               xaxis=dict(tickangle=-20))
            st.plotly_chart(fig, use_container_width=True)

        # Probability by decade and technology
        st.markdown("#### Predicted on-time probability by start decade")
        decade_tech = (
            comp_preds.groupby(["start_decade","technology_family"])["prob_on_time"]
            .mean().reset_index()
            .rename(columns={"start_decade":"Decade","technology_family":"Technology",
                              "prob_on_time":"Avg prob on-time"})
        )
        fig2 = px.bar(
            decade_tech, x="Decade", y="Avg prob on-time",
            color="Technology", barmode="group",
            template="plotly_white",
            labels={"Avg prob on-time":"Avg predicted prob on-time"},
        )
        fig2.update_layout(margin=dict(t=10), xaxis=dict(type="category"))
        st.plotly_chart(fig2, use_container_width=True)

        st.caption(
            "Takeaway: 1960s–80s first-of-a-kind builds had lower on-time probability. "
            "Series-built designs in later decades (CPR-1000, VVER-1000) improved. "
            "Recent advanced designs (SMR, HPR-1000) have high predicted probability "
            "driven by modern construction management — but less validation data."
        )

        st.divider()
        st.markdown("**Full prediction table**")
        st.dataframe(
            comp_preds.sort_values("prob_on_time", ascending=False)
            .rename(columns={
                "reactor_name":"Project","country":"Country",
                "technology_family":"Technology","capacity_mwe":"MWe",
                "start_decade":"Start decade","completed_on_time":"Label",
                "predicted_on_time":"Predicted","prob_on_time":"Prob on-time",
                "actual_build_years":"Actual build years",
            }),
            use_container_width=True, hide_index=True,
        )

        st.divider()

    else:
        st.warning("Real completion classifier not available. Run `python run_pipeline.py`.")

    # ── HEURISTIC SCORING (legacy) ─────────────────────────────────────────────
    with st.expander("Legacy heuristic risk scoring (pipeline projects)"):
        st.caption(
            "Maturity and delay risk scores for current pipeline projects. "
            "These are auditable heuristics — not ML predictions. "
            "Use the completion classifier above for probability estimates."
        )
        if not risk.empty:
            fig3 = px.scatter(
                risk,
                x="project_maturity_score", y="delay_risk_score",
                size="capacity_mwe", color="risk_level",
                hover_name="reactor_name",
                hover_data=["country","technology_family","realization_probability"],
                color_discrete_map={"Low":"#10b981","Medium":"#f59e0b","High":"#ef4444"},
                labels={"project_maturity_score":"Maturity score",
                        "delay_risk_score":"Delay risk score",
                        "risk_level":"Risk"},
                template="plotly_white",
                size_max=40,
            )
            fig3.update_layout(margin=dict(t=10))
            st.plotly_chart(fig3, use_container_width=True)
            st.dataframe(
                risk.sort_values("delay_risk_score", ascending=False),
                use_container_width=True, hide_index=True,
            )

    _method(
        data="project_completion_dataset.csv — 418 labeled projects derived from "
             "reactors_master.csv construction_start_date and commercial_operation_date "
             "(real IAEA/WNA historical dates)",
        features="technology_family · reactor_type · capacity_mwe · start_decade · "
                 "source_confidence (5 features)",
        model="Gradient Boosting Classifier (best) vs Logistic Regression / RF / XGBoost. "
              "CV F1 = 0.882, ROC-AUC = 0.958. "
              "StratifiedKFold(k=5). class_weight='balanced' for imbalanced labels.",
        notes="Labels are real: 1 = completed in ≤10 years, 0 = delayed or at-risk. "
              "NOT a heuristic — derived from observed construction dates. "
              "Limitation: our reactor dataset is a curated sample, not the full IAEA PRIS history.",
    )
