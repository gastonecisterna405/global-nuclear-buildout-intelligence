from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.dashboard.page_renderers._methodology import section as _method

STATUS_COLORS = {
    "Operating":    "#2563eb",
    "Construction": "#f59e0b",
    "Planned":      "#10b981",
    "Proposed":     "#8b5cf6",
    "Shutdown":     "#ef4444",
}


def _kpi(col, label, value):
    col.metric(label, value)


def render(
    reactors: pd.DataFrame,
    countries: pd.DataFrame,
    pipeline: pd.DataFrame,
    taxonomy: pd.DataFrame,
) -> None:
    st.subheader("Exploratory Data Analysis — Global Nuclear Fleet")

    # ── 1. Global snapshot ────────────────────────────────────────────────────
    st.markdown("### 1. Global Snapshot")
    op = reactors[reactors.status_group == "Operating"]
    uc = reactors[reactors.status_group == "Construction"]

    c = st.columns(5)
    c[0].metric("Total records",        f"{len(reactors):,}")
    c[1].metric("Countries",            reactors.country.nunique())
    c[2].metric("Operating GWe",        f"{op.capacity_mwe.sum()/1000:,.1f}")
    c[3].metric("Under construction GWe", f"{uc.capacity_mwe.sum()/1000:,.1f}")
    c[4].metric("Pipeline projects",    len(pipeline))

    # ── 2. Capacity by country and status ─────────────────────────────────────
    st.markdown("### 2. Capacity by Country")

    tab1, tab2 = st.tabs(["Operating (top 15)", "All statuses"])

    with tab1:
        cap = (
            op.groupby("country")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).head(15).reset_index()
        )
        cap.columns = ["Country", "GWe"]
        fig = px.bar(cap, x="Country", y="GWe", template="plotly_white",
                     color_discrete_sequence=["#2563eb"])
        fig.update_layout(xaxis_title="", margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)

    with tab2:
        all_cap = (
            reactors[reactors.status_group.isin(["Operating","Construction","Planned","Proposed"])]
            .groupby(["country","status_group"])["capacity_mwe"].sum().div(1000)
            .reset_index()
        )
        all_cap.columns = ["Country", "Status", "GWe"]
        all_cap = all_cap.sort_values("GWe", ascending=False)
        fig2 = px.bar(all_cap, x="Country", y="GWe", color="Status",
                      color_discrete_map=STATUS_COLORS,
                      template="plotly_white", barmode="stack")
        fig2.update_layout(xaxis_title="", margin=dict(t=10),
                           xaxis=dict(tickangle=-40), height=420)
        st.plotly_chart(fig2, use_container_width=True)

    # ── 3. Technology mix ─────────────────────────────────────────────────────
    st.markdown("### 3. Technology Mix")

    left, right = st.columns(2)
    with left:
        st.caption("Operating fleet — by capacity (GWe)")
        tech = (
            op.groupby("technology_family")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).reset_index()
        )
        tech.columns = ["Technology", "GWe"]
        fig = px.pie(tech, names="Technology", values="GWe",
                     hole=0.35, template="plotly_white")
        fig.update_layout(margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.caption("Pipeline — construction + planned (by capacity)")
        pipe_tech = (
            pipeline[pipeline.status_group.isin(["Construction","Planned"])]
            .groupby("technology_family")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).reset_index()
        )
        pipe_tech.columns = ["Technology", "GWe"]
        fig2 = px.bar(pipe_tech, x="Technology", y="GWe",
                      template="plotly_white",
                      color_discrete_sequence=["#f59e0b"])
        fig2.update_layout(xaxis_title="", margin=dict(t=10),
                           xaxis=dict(tickangle=-25))
        st.plotly_chart(fig2, use_container_width=True)

    st.caption(
        "Takeaway: LWR families (PWR/VVER/AP1000/EPR) dominate the operating fleet. "
        "The pipeline has a higher share of advanced designs (HPR-1000, VVER-1200, SMR). "
        "Whether this shifts the fleet mix depends on financing and licensing timelines."
    )

    # ── 4. Fleet age analysis ─────────────────────────────────────────────────
    st.markdown("### 4. Fleet Age Analysis")

    op_dated = op.dropna(subset=["age_years"])
    median_age = op_dated["age_years"].median()

    left, right = st.columns(2)
    with left:
        fig = px.histogram(op_dated, x="age_years", nbins=30, template="plotly_white",
                           labels={"age_years": "Age (years)", "count": "Units"},
                           color_discrete_sequence=["#2563eb"])
        fig.add_vline(x=median_age, line_dash="dash", line_color="red",
                      annotation_text=f"Median: {median_age:.0f} yr",
                      annotation_position="top right")
        fig.update_layout(margin=dict(t=10), xaxis_title="Age (years)")
        st.plotly_chart(fig, use_container_width=True)

    with right:
        age_c = (
            op_dated.groupby("country")["age_years"].mean()
            .sort_values(ascending=False).head(15).reset_index()
        )
        age_c.columns = ["Country", "Avg age (yr)"]
        fig2 = px.bar(age_c, x="Country", y="Avg age (yr)",
                      template="plotly_white",
                      color="Avg age (yr)", color_continuous_scale="Reds")
        fig2.update_layout(margin=dict(t=10), xaxis_title="",
                           xaxis=dict(tickangle=-35), coloraxis_showscale=False)
        st.plotly_chart(fig2, use_container_width=True)

    pct_over_40 = (op_dated["age_years"] >= 40).mean() * 100
    st.caption(
        f"Median fleet age: **{median_age:.0f} years**. "
        f"{pct_over_40:.0f}% of operating units are 40+ years old. "
        "Countries with the oldest fleets face capacity replacement pressure — "
        "a structural driver of new project activity."
    )

    # ── 5. Historical buildout ─────────────────────────────────────────────────
    st.markdown("### 5. Historical Buildout by Decade")

    r_dated = reactors[reactors.commercial_operation_date.notna()].copy()
    r_dated["year"] = pd.to_datetime(r_dated["commercial_operation_date"]).dt.year
    r_dated["decade"] = (r_dated["year"] // 10) * 10

    by_dec = (
        r_dated.groupby(["decade","technology_family"])["capacity_mwe"]
        .sum().div(1000).reset_index()
    )
    by_dec.columns = ["Decade","Technology","GWe"]

    fig = px.bar(by_dec, x="Decade", y="GWe", color="Technology",
                 template="plotly_white", barmode="stack",
                 labels={"Decade": "Decade", "GWe": "Capacity commissioned (GWe)"})
    fig.update_layout(margin=dict(t=10), xaxis=dict(type="category"))
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "1970s–80s: peak buildout era. 1990s–2000s: sharp slowdown after TMI, Chernobyl, "
        "cost overruns. 2010s–20s: China-led recovery with new designs. "
        "Recent years show EPR and AP1000 first-of-a-kind commissioning."
    )

    # ── 6. Nuclear share by country ───────────────────────────────────────────
    st.markdown("### 6. Nuclear Share of Electricity")

    c_share = countries.dropna(subset=["nuclear_share_percent"]).copy()
    c_share = c_share[c_share.nuclear_share_percent > 0].sort_values(
        "nuclear_share_percent", ascending=False
    )
    fig = px.bar(c_share, x="country", y="nuclear_share_percent",
                 color="nuclear_share_percent",
                 color_continuous_scale="Blues",
                 labels={"country":"Country","nuclear_share_percent":"Nuclear share (%)"},
                 template="plotly_white")
    fig.update_layout(margin=dict(t=10), xaxis_title="",
                      xaxis=dict(tickangle=-40), coloraxis_showscale=False)
    fig.add_hline(y=30, line_dash="dot", line_color="orange",
                  annotation_text="30% threshold", annotation_position="top right")
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "France leads with ~65% nuclear share. Countries above 30% are highly dependent "
        "on nuclear for baseload. New entrants (Turkey, Egypt, Bangladesh) are at 0% "
        "but have UC projects — their nuclear share will appear when plants commission."
    )

    # ── 7. Region breakdown ───────────────────────────────────────────────────
    st.markdown("### 7. Regional Breakdown")

    left, right = st.columns(2)
    with left:
        st.caption("Operating capacity by region (GWe)")
        reg = (
            op.groupby("region")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).reset_index()
        )
        reg.columns = ["Region", "GWe"]
        fig = px.pie(reg, names="Region", values="GWe", hole=0.35,
                     template="plotly_white")
        fig.update_layout(margin=dict(t=10))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.caption("Under-construction capacity by region (GWe)")
        reg_uc = (
            uc.groupby("region")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).reset_index()
        )
        reg_uc.columns = ["Region", "GWe"]
        fig2 = px.bar(reg_uc, x="Region", y="GWe",
                      template="plotly_white",
                      color_discrete_sequence=["#f59e0b"])
        fig2.update_layout(margin=dict(t=10), xaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)

    # ── 8. Vendor and design landscape ────────────────────────────────────────
    st.markdown("### 8. Vendor Landscape")

    left, right = st.columns(2)
    with left:
        st.caption("Operating fleet — top vendors by GWe supplied")
        vendor = (
            op.groupby("vendor")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).head(12).reset_index()
        )
        vendor.columns = ["Vendor", "GWe"]
        fig = px.bar(vendor, x="GWe", y="Vendor", orientation="h",
                     template="plotly_white",
                     color_discrete_sequence=["#2563eb"])
        fig.update_layout(margin=dict(t=10), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.caption("Pipeline — top vendors by GWe under construction / planned")
        pipe_vendor = (
            pipeline[pipeline.status_group.isin(["Construction","Planned"])]
            .merge(reactors[["reactor_id","vendor"]], on="reactor_id", how="left")
            .groupby("vendor")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).head(12).reset_index()
        ) if "vendor" not in pipeline.columns else (
            pipeline[pipeline.status_group.isin(["Construction","Planned"])]
            .groupby("vendor")["capacity_mwe"].sum().div(1000)
            .sort_values(ascending=False).head(12).reset_index()
        )
        pipe_vendor.columns = ["Vendor", "GWe"]
        fig2 = px.bar(pipe_vendor, x="GWe", y="Vendor", orientation="h",
                      template="plotly_white",
                      color_discrete_sequence=["#f59e0b"])
        fig2.update_layout(margin=dict(t=10), yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig2, use_container_width=True)

    # ── 9. Construction duration ───────────────────────────────────────────────
    st.markdown("### 9. Construction Duration by Reactor Type")

    r_both = reactors[
        reactors.construction_start_date.notna()
        & reactors.commercial_operation_date.notna()
    ].copy()
    r_both["construction_start_date"] = pd.to_datetime(r_both["construction_start_date"])
    r_both["commercial_operation_date"] = pd.to_datetime(r_both["commercial_operation_date"])
    r_both["build_years"] = (
        (r_both["commercial_operation_date"] - r_both["construction_start_date"])
        .dt.days / 365.25
    )
    r_both = r_both[(r_both["build_years"] > 1) & (r_both["build_years"] < 30)]

    if not r_both.empty:
        median_build = r_both["build_years"].median()
        fig = px.box(r_both, x="technology_family", y="build_years",
                     color="technology_family", template="plotly_white",
                     labels={"technology_family": "Technology",
                             "build_years": "Construction duration (years)"},
                     points="all")
        fig.add_hline(y=median_build, line_dash="dash", line_color="red",
                      annotation_text=f"Overall median: {median_build:.1f} yr")
        fig.update_layout(margin=dict(t=10), xaxis_title="",
                          showlegend=False, xaxis=dict(tickangle=-20))
        st.plotly_chart(fig, use_container_width=True)
        st.caption(
            f"Median construction duration across all reactor types: **{median_build:.1f} years**. "
            "Large first-of-a-kind units (EPR, AP1000) show longer durations. "
            "Series-built plants (CPR-1000 in China, VVER-1000 in Russia) trend shorter."
        )

    # ── 10. Capacity factor & electricity scenarios ────────────────────────────
    st.markdown("### 10. Generation Potential at Different Capacity Factors")

    gwe_op = op["capacity_mwe"].sum() / 1000
    cf_range = [0.70, 0.80, 0.85, 0.90, 0.93]
    gen_data = pd.DataFrame({
        "Capacity factor": [f"{int(cf*100)}%" for cf in cf_range],
        "TWh / year": [round(gwe_op * cf * 8.76, 0) for cf in cf_range],
    })
    fig = px.bar(gen_data, x="Capacity factor", y="TWh / year",
                 template="plotly_white",
                 color_discrete_sequence=["#10b981"],
                 text="TWh / year")
    fig.update_traces(textposition="outside")
    fig.update_layout(margin=dict(t=30), yaxis_title="TWh / year")
    st.plotly_chart(fig, use_container_width=True)
    st.caption(
        f"Operating fleet: **{gwe_op:,.1f} GWe**. "
        "At 85% capacity factor (typical for PWRs), this corresponds to "
        f"**{gwe_op * 0.85 * 8.76:,.0f} TWh/year** — "
        "approximately 10% of global electricity generation."
    )

    _method(
        data="reactors_master.csv (full fleet) · reactor_pipeline.csv (UC/Planned) · "
             "country_nuclear_profile.csv (nuclear share, GDP) · technology_taxonomy.csv",
        features="capacity_mwe by status/country/technology/decade · age_years · "
                 "nuclear_share_percent · build duration (commercial_operation - construction_start) · "
                 "vendor · region",
        notes="All EDA — descriptive statistics and visualizations only. No predictive model.",
    )
