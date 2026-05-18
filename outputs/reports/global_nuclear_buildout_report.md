# Global Nuclear Buildout Intelligence Report
*Generated: 2026-05-18 | Dataset: 443 reactor records, 34 countries*

---

> This report is generated from a curated sample dataset based on IAEA PRIS / WNA / GEM public records. It is a strategic analytics tool, not an official forecast or investment recommendation. Numbers are representative but not source-of-record.

---

## 1. Executive Summary

The global nuclear fleet comprises **379 operating units** across **34 countries**, delivering approximately **2,577 TWh/year** at an 85% capacity factor (346.0 GWe nameplate). A construction pipeline of **35 units** (37.0 GWe) represents the most certain near-term capacity addition. An additional 10 planned (9.5 GWe) and 5 proposed (4.0 GWe) projects form the longer-horizon pipeline.

The fleet is aging — median unit age is **39 years**, with **49%** of operating reactors aged 40 or more. This creates simultaneous pressure for life extensions and replacements, and is a key structural driver of new project activity in mature nuclear countries.

Under the Base scenario, total nuclear capacity reaches **374.4 GWe** by 2050, generating approximately **2,821 TWh/year** — representing nuclear's continued but moderate role in a decarbonising grid.

---

## 2. Global Fleet Overview

| Metric | Value |
|---|---|
| Operating units | 379 |
| Operating capacity | 346.0 GWe |
| Under construction units | 35 |
| Under construction capacity | 37.0 GWe |
| Planned capacity | 9.5 GWe |
| Proposed capacity | 4.0 GWe |
| Countries with nuclear records | 34 |
| Median fleet age | 39 years |
| Units aged 40+ years | 185 (49%) |
| Estimated annual generation (85% CF) | 2,577 TWh/yr |

### Top 5 countries by operating capacity
United States (80.1 GWe), France (62.0 GWe), China (51.7 GWe), Russia (29.0 GWe), South Korea (23.8 GWe)

### Top 5 countries by pipeline capacity (UC + Planned)
China (12.3 GWe), United Kingdom (4.6 GWe), Turkey (4.5 GWe), India (4.3 GWe), Russia (3.8 GWe)

---

## 3. Technology Mix

**Light Water Reactor** dominates the operating fleet, accounting for **312.3 GWe** (90% of total operating capacity). This reflects 70 years of commercial deployment and accumulated regulatory familiarity — the primary reason LWR technologies receive the highest maturity scores in the platform.

### Technology family breakdown (operating fleet)

| Technology | GWe | Share |
|---|---|---|
| Light Water Reactor | 312.3 | 90.2% |
| Heavy Water Reactor | 21.2 | 6.1% |
| Other/Unclassified | 11.0 | 3.2% |
| Fast Reactor | 1.3 | 0.4% |
| Gas-Cooled Reactor | 0.2 | 0.1% |

### Advanced technology pipeline

**1.5 GWe** of advanced technology capacity (SMR, Gen IV, Gas-cooled) is in the construction or planned pipeline. This represents a strategic signal rather than a near-term certainty — deployment history for most of these designs remains limited. The platform treats them as scenario inputs with explicit maturity discounts.

---

## 4. Reactor Pipeline Analysis

The pipeline contains **50 projects** with a combined capacity of **50.5 GWe**:
- **Under construction (35 units)**: Highest realization confidence. Weighted by technology maturity, country experience, and GDP context.
- **Planned (10 units)**: Moderate confidence. Requires financing, licensing, and site approval.
- **Proposed (5 units)**: Early-stage indicators. Best interpreted as strategic signals.

### Project maturity distribution

Average project maturity score across the pipeline: **73.8 / 100** (higher = more confident in realization).

---

## 5. Project Risk Assessment

| Risk Level | Projects | Avg. delay risk score |
|---|---|---|
| High | 0 | nan |
| Medium | 13 | 45.1 |
| Low | 37 | 22.5 |

Average realization probability across all pipeline projects: **74%**

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
| Commercial (≥75) | PWR, BWR, PHWR, VVER, EPR, AP1000 | 75–100 |
| Commercialising (55–74) |  | 55–74 |
| Demonstration (30–54) | SMR-LWR, HTGR, SFR | 30–54 |
| Early-stage (<30) | LFR, MSR, Thorium concepts, Microreactor | <30 |

**Lowest maturity**: Thorium concepts, Microreactor, MSR
**Highest maturity**: PWR, BWR, PHWR

---

## 7. Electricity Supply Scenarios

Scenarios are built using: `TWh/year = capacity_GW × capacity_factor × 8.76 × realization_adjustment`

| Scenario | 2050 GWe | 2050 TWh/yr | vs. today |
|---|---|---|---|
| Conservative | 366.9 | 2,764 | ++7% |
| Base | 374.4 | 2,821 | ++9% |
| Accelerated | 382.0 | 2,878 | ++12% |

*Today's estimated generation at 85% CF: 2,577 TWh/yr*

Key scenario assumptions:
- **Conservative**: 55% of pipeline capacity realized by expected operation year.
- **Base**: 75% realization probability applied.
- **Accelerated**: 95% realization probability — requires policy support, financing, and supply chain capacity beyond current trajectories.

---

## 8. Policy and NLP Intelligence

Policy text tagging was applied to 10 country policy documents across 10 topic categories: SMR, Gen IV, Fast Reactor, Molten Salt, Thorium, Financing, Delay Risk, Energy Security, Decarbonization, and Industrial Heat.

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

1. **Capacity cliff risk**: With 49% of the operating fleet aged 40+, replacement demand is structural and growing — regardless of new build policy.
2. **China dominance in new build**: China accounts for the majority of global UC capacity and is the primary driver of near-term additions.
3. **Advanced technology gap**: SMR and Gen IV designs represent a significant share of pipeline *by count* but limited share *by capacity*. Deployment evidence lags vendor claims by a decade or more.
4. **New entrant markets**: Turkey, Egypt, and Bangladesh represent first-time nuclear programs — they carry high delay risk but also signal growing global demand.
5. **Energy security narrative**: Policy text analysis confirms energy security and decarbonization framing are the primary drivers of new programs, with financing and supply chain identified as key barriers.

---

*Sources: IAEA PRIS, WNA, Global Energy Monitor (curated sample). "
"See Data Quality page for source coverage and confidence ratings.*
