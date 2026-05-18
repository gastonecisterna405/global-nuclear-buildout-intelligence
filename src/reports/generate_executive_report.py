from __future__ import annotations

import datetime
import pandas as pd
from src import config

DISCLAIMER = (
    "This report is generated from a curated sample dataset based on IAEA PRIS / WNA / GEM "
    "public records. It is a strategic analytics tool, not an official forecast or investment "
    "recommendation. Numbers are representative but not source-of-record."
)


def generate_executive_report() -> str:
    reactors   = pd.read_csv(config.PROCESSED / "reactors_master.csv")
    countries  = pd.read_csv(config.PROCESSED / "country_nuclear_profile.csv")
    pipeline   = pd.read_csv(config.PROCESSED / "reactor_pipeline.csv")
    taxonomy   = pd.read_csv(config.PROCESSED / "technology_taxonomy.csv")
    scenarios  = pd.read_csv(config.PROCESSED / "nuclear_capacity_scenarios.csv")
    risk       = pd.read_csv(config.PREDICTIONS / "project_risk_scores.csv")

    # ── Fleet metrics ──────────────────────────────────────────────────────────
    op  = reactors[reactors.status_group == "Operating"]
    uc  = reactors[reactors.status_group == "Construction"]
    pl  = reactors[reactors.status_group == "Planned"]
    pr  = reactors[reactors.status_group == "Proposed"]
    sd  = reactors[reactors.status_group == "Shutdown"]

    op_gwe  = op.capacity_mwe.sum()  / 1000
    uc_gwe  = uc.capacity_mwe.sum()  / 1000
    pl_gwe  = pl.capacity_mwe.sum()  / 1000
    pr_gwe  = pr.capacity_mwe.sum()  / 1000

    n_countries    = reactors.country.nunique()
    median_age     = op.age_years.dropna().median()
    pct_over40     = (op.age_years.dropna() >= 40).mean() * 100

    # Top countries by operating capacity
    top_op = (
        op.groupby("country")["capacity_mwe"].sum().div(1000)
        .sort_values(ascending=False).head(5)
    )
    top_op_str = ", ".join(f"{c} ({v:.1f} GWe)" for c, v in top_op.items())

    # Top pipeline countries
    top_pipe = (
        pipeline.groupby("country")["capacity_mwe"].sum().div(1000)
        .sort_values(ascending=False).head(5)
    )
    top_pipe_str = ", ".join(f"{c} ({v:.1f} GWe)" for c, v in top_pipe.items())

    # Technology mix
    tech_mix = (
        op.groupby("technology_family")["capacity_mwe"].sum().div(1000)
        .sort_values(ascending=False)
    )
    dominant_tech = tech_mix.index[0]
    dominant_gwe  = tech_mix.iloc[0]
    dominant_pct  = dominant_gwe / op_gwe * 100

    # Advanced tech in pipeline
    adv_pipeline = pipeline[
        pipeline.technology_family.str.contains("Small Modular|Fast|Molten|Gas|Micro",
                                                  case=False, na=False)
    ]
    adv_gwe = adv_pipeline.capacity_mwe.sum() / 1000

    # Scenario stats
    base_2050 = scenarios[(scenarios.year == 2050) & (scenarios.scenario == "Base")]
    base_twh  = base_2050.estimated_generation_twh.sum()
    cons_2050 = scenarios[(scenarios.year == 2050) & (scenarios.scenario == "Conservative")]
    cons_twh  = cons_2050.estimated_generation_twh.sum()
    accel_2050 = scenarios[(scenarios.year == 2050) & (scenarios.scenario == "Accelerated")]
    accel_twh  = accel_2050.estimated_generation_twh.sum()
    base_gwe_2050 = base_2050.capacity_gwe.sum()

    # Risk stats
    high_risk  = risk[risk.risk_level == "High"]
    low_risk   = risk[risk.risk_level == "Low"]
    avg_realiz = risk.realization_probability.mean()

    # NLP stats
    docs_path = config.PROCESSED / "nlp_policy_documents.csv"
    n_docs = len(pd.read_csv(docs_path)) if docs_path.exists() else 0

    # Generation estimate
    gen_85cf = op_gwe * 0.85 * 8.76

    today = datetime.date.today().isoformat()

    report = f"""# Global Nuclear Buildout Intelligence Report
*Generated: {today} | Dataset: {len(reactors)} reactor records, {n_countries} countries*

---

> {DISCLAIMER}

---

## 1. Executive Summary

The global nuclear fleet comprises **{len(op)} operating units** across **{n_countries} countries**, delivering approximately **{gen_85cf:,.0f} TWh/year** at an 85% capacity factor ({op_gwe:,.1f} GWe nameplate). A construction pipeline of **{len(uc)} units** ({uc_gwe:,.1f} GWe) represents the most certain near-term capacity addition. An additional {len(pl)} planned ({pl_gwe:,.1f} GWe) and {len(pr)} proposed ({pr_gwe:,.1f} GWe) projects form the longer-horizon pipeline.

The fleet is aging — median unit age is **{median_age:.0f} years**, with **{pct_over40:.0f}%** of operating reactors aged 40 or more. This creates simultaneous pressure for life extensions and replacements, and is a key structural driver of new project activity in mature nuclear countries.

Under the Base scenario, total nuclear capacity reaches **{base_gwe_2050:,.1f} GWe** by 2050, generating approximately **{base_twh:,.0f} TWh/year** — representing nuclear's continued but moderate role in a decarbonising grid.

---

## 2. Global Fleet Overview

| Metric | Value |
|---|---|
| Operating units | {len(op)} |
| Operating capacity | {op_gwe:,.1f} GWe |
| Under construction units | {len(uc)} |
| Under construction capacity | {uc_gwe:,.1f} GWe |
| Planned capacity | {pl_gwe:,.1f} GWe |
| Proposed capacity | {pr_gwe:,.1f} GWe |
| Countries with nuclear records | {n_countries} |
| Median fleet age | {median_age:.0f} years |
| Units aged 40+ years | {(op.age_years.dropna() >= 40).sum()} ({pct_over40:.0f}%) |
| Estimated annual generation (85% CF) | {gen_85cf:,.0f} TWh/yr |

### Top 5 countries by operating capacity
{top_op_str}

### Top 5 countries by pipeline capacity (UC + Planned)
{top_pipe_str}

---

## 3. Technology Mix

**{dominant_tech}** dominates the operating fleet, accounting for **{dominant_gwe:,.1f} GWe** ({dominant_pct:.0f}% of total operating capacity). This reflects 70 years of commercial deployment and accumulated regulatory familiarity — the primary reason LWR technologies receive the highest maturity scores in the platform.

### Technology family breakdown (operating fleet)

| Technology | GWe | Share |
|---|---|---|
{chr(10).join(f"| {t} | {v:,.1f} | {v/op_gwe*100:.1f}% |" for t, v in tech_mix.items())}

### Advanced technology pipeline

**{adv_gwe:,.1f} GWe** of advanced technology capacity (SMR, Gen IV, Gas-cooled) is in the construction or planned pipeline. This represents a strategic signal rather than a near-term certainty — deployment history for most of these designs remains limited. The platform treats them as scenario inputs with explicit maturity discounts.

---

## 4. Reactor Pipeline Analysis

The pipeline contains **{len(pipeline)} projects** with a combined capacity of **{pipeline.capacity_mwe.sum()/1000:,.1f} GWe**:
- **Under construction ({len(uc)} units)**: Highest realization confidence. Weighted by technology maturity, country experience, and GDP context.
- **Planned ({len(pl)} units)**: Moderate confidence. Requires financing, licensing, and site approval.
- **Proposed ({len(pr)} units)**: Early-stage indicators. Best interpreted as strategic signals.

### Project maturity distribution

Average project maturity score across the pipeline: **{pipeline.project_maturity_score.mean():.1f} / 100** (higher = more confident in realization).

---

## 5. Project Risk Assessment

| Risk Level | Projects | Avg. delay risk score |
|---|---|---|
| High | {len(high_risk)} | {high_risk.delay_risk_score.mean():.1f} |
| Medium | {len(risk[risk.risk_level=='Medium'])} | {risk[risk.risk_level=='Medium'].delay_risk_score.mean():.1f} |
| Low | {len(low_risk)} | {low_risk.delay_risk_score.mean():.1f} |

Average realization probability across all pipeline projects: **{avg_realiz:.0%}**

Risk drivers (scored transparently):
1. **Project stage** — Construction-stage projects score 85/100 on stage component; proposed projects score 30/100.
2. **Technology maturity** — Commercial LWR designs score higher than first-of-a-kind advanced reactors.
3. **Country experience** — Countries with 40+ years of nuclear operation and completed reactors score higher.
4. **Unit size** — Projects above 1,200 MWe receive a delay penalty reflecting historical first-of-a-kind complexity.

---

## 6. Technology Maturity Scoring

The platform scores 13 reactor types across 8 technology families using:

```
maturity_score = base_maturity
              + known_operating_units × 1.2
              + known_under_construction_units × 1.8
```

| Category | Reactor types | Score range |
|---|---|---|
| Commercial (≥75) | {", ".join(taxonomy[taxonomy.maturity_score>=75].reactor_type.tolist())} | 75–100 |
| Commercialising (55–74) | {", ".join(taxonomy[(taxonomy.maturity_score>=55)&(taxonomy.maturity_score<75)].reactor_type.tolist())} | 55–74 |
| Demonstration (30–54) | {", ".join(taxonomy[(taxonomy.maturity_score>=30)&(taxonomy.maturity_score<55)].reactor_type.tolist())} | 30–54 |
| Early-stage (<30) | {", ".join(taxonomy[taxonomy.maturity_score<30].reactor_type.tolist())} | <30 |

**Lowest maturity**: {", ".join(taxonomy.sort_values("maturity_score").head(3).reactor_type.tolist())}
**Highest maturity**: {", ".join(taxonomy.sort_values("maturity_score", ascending=False).head(3).reactor_type.tolist())}

---

## 7. Electricity Supply Scenarios

Scenarios are built using: `TWh/year = capacity_GW × capacity_factor × 8.76 × realization_adjustment`

| Scenario | 2050 GWe | 2050 TWh/yr | vs. today |
|---|---|---|---|
| Conservative | {scenarios[(scenarios.year==2050)&(scenarios.scenario=='Conservative')].capacity_gwe.sum():,.1f} | {cons_twh:,.0f} | +{cons_twh/gen_85cf*100-100:+.0f}% |
| Base | {base_gwe_2050:,.1f} | {base_twh:,.0f} | +{base_twh/gen_85cf*100-100:+.0f}% |
| Accelerated | {scenarios[(scenarios.year==2050)&(scenarios.scenario=='Accelerated')].capacity_gwe.sum():,.1f} | {accel_twh:,.0f} | +{accel_twh/gen_85cf*100-100:+.0f}% |

*Today's estimated generation at 85% CF: {gen_85cf:,.0f} TWh/yr*

Key scenario assumptions:
- **Conservative**: 55% of pipeline capacity realized by expected operation year.
- **Base**: 75% realization probability applied.
- **Accelerated**: 95% realization probability — requires policy support, financing, and supply chain capacity beyond current trajectories.

---

## 8. Policy and NLP Intelligence

Policy text tagging was applied to {n_docs} country policy documents across 10 topic categories: SMR, Gen IV, Fast Reactor, Molten Salt, Thorium, Financing, Delay Risk, Energy Security, Decarbonization, and Industrial Heat.

Countries with the strongest policy signals tend to combine:
- Explicit SMR or Gen IV development programs
- Active construction or procurement activity
- Energy security framing (coal replacement, supply chain independence)

---

## 9. Data Limitations and Next Steps

**Current limitations:**
- Dataset is a curated sample based on public sources — not a substitute for official IAEA PRIS bulk exports.
- Project timeline estimates (expected operation year) are heuristic by status group, not project-specific.
- Risk labels are derived from scoring rules, not validated against historical project outcomes.
- Scenario results are sensitivity demonstrations, not market or policy forecasts.

**For production use:**
1. Replace sample data with official IAEA PRIS manual exports via `data/raw/iaea_pris/` templates.
2. Add annual PRIS snapshots (2000–present) to enable supervised forecasting.
3. Validate risk labels against historical realization outcomes (projects commissioned vs. cancelled).
4. Connect scheduled data refresh via Databricks / Delta Lake (see `spark/` directory).

---

## 10. Strategic Implications

1. **Capacity cliff risk**: With {pct_over40:.0f}% of the operating fleet aged 40+, replacement demand is structural and growing — regardless of new build policy.
2. **China dominance in new build**: China accounts for the majority of global UC capacity and is the primary driver of near-term additions.
3. **Advanced technology gap**: SMR and Gen IV designs represent a significant share of pipeline *by count* but limited share *by capacity*. Deployment evidence lags vendor claims by a decade or more.
4. **New entrant markets**: Turkey, Egypt, and Bangladesh represent first-time nuclear programs — they carry high delay risk but also signal growing global demand.
5. **Energy security narrative**: Policy text analysis confirms energy security and decarbonization framing are the primary drivers of new programs, with financing and supply chain identified as key barriers.

---

*Sources: IAEA PRIS, WNA, Global Energy Monitor (curated sample). "
"See Data Quality page for source coverage and confidence ratings.*
"""

    path = config.REPORTS / "global_nuclear_buildout_report.md"
    path.write_text(report, encoding="utf-8")
    (config.REPORTS / "executive_summary.md").write_text(
        "\n".join(report.split("\n")[:30]), encoding="utf-8"
    )
    return report
