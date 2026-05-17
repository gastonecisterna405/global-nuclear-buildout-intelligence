from __future__ import annotations
import pandas as pd

def summarize_policy_signals(docs: pd.DataFrame) -> str:
    top = docs.sort_values("policy_support_signal", ascending=False).head(3)
    return "; ".join(f"{r.country}: {r.detected_topics}" for _, r in top.iterrows())
