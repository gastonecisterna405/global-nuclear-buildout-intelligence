from __future__ import annotations
import pandas as pd
from src import config
from src.nlp.keyword_extraction import extract_keywords
from src.nlp.topic_tagging import tag_topics

def run_nlp_pipeline() -> tuple[pd.DataFrame, pd.DataFrame]:
    docs = pd.read_csv(config.RAW / "sample" / "policy_documents_raw.csv")
    topic_rows = []
    enriched = []
    for _, row in docs.iterrows():
        tags = tag_topics(row["text"])
        score = min(100, 20 + sum(tags.values()) * 9)
        enriched.append({**row.to_dict(), "extracted_keywords": "", "detected_topics": ",".join([k for k,v in tags.items() if v]), "smr_signal": tags["SMR"], "geniv_signal": tags["Gen IV"], "financing_signal": tags["Financing"], "policy_support_signal": score, "delay_risk_signal": tags["Delay Risk"], "sentiment_or_policy_score": score})
        for topic, val in tags.items():
            topic_rows.append({"document_id": row["document_id"], "country": row["country"], "topic": topic, "present": val})
    docs_out = pd.DataFrame(enriched)
    kw = extract_keywords(docs)
    top_kw = kw.groupby(["country","term"], as_index=False)["count"].sum().sort_values("count", ascending=False)
    topics = pd.DataFrame(topic_rows)
    docs_out.to_csv(config.PROCESSED / "nlp_policy_documents.csv", index=False)
    kw.to_csv(config.ANALYTICS / "nlp_keywords.csv", index=False)
    top_kw.to_csv(config.ANALYTICS / "top_terms_by_country.csv", index=False)
    topics.to_csv(config.ANALYTICS / "topic_distribution.csv", index=False)
    topics.pivot_table(index="country", columns="topic", values="present", aggfunc="max", fill_value=0).to_csv(config.ANALYTICS / "country_policy_signals.csv")
    topics.to_csv(config.ANALYTICS / "technology_mentions.csv", index=False)
    return docs_out, topics
