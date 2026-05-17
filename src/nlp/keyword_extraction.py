from __future__ import annotations
from collections import Counter
import pandas as pd
from src.nlp.nuclear_text_cleaning import clean_text

DEFAULT_STOPWORDS = set("the and of to in for with a an is are be as by or on from this that into it at".split())

def tokenize(text: str) -> list[str]:
    try:
        import nltk
        from nltk.corpus import stopwords
        try:
            stops = set(stopwords.words("english"))
        except LookupError:
            stops = DEFAULT_STOPWORDS
    except Exception:
        stops = DEFAULT_STOPWORDS
    return [t for t in clean_text(text).split() if len(t) > 2 and t not in stops]

def extract_keywords(docs: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in docs.iterrows():
        counts = Counter(tokenize(row["text"]))
        for term, count in counts.most_common(20):
            rows.append({"document_id": row["document_id"], "country": row["country"], "term": term, "count": count})
    return pd.DataFrame(rows)
