from __future__ import annotations

TOPICS = {
    "SMR": ["smr", "small modular", "bwrx", "carem", "microreactor"],
    "Gen IV": ["gen iv", "advanced reactor", "high temperature", "fast reactor", "closed fuel"],
    "Molten Salt": ["molten salt", "msr", "salt"],
    "Thorium": ["thorium", "u-233"],
    "Fast Reactor": ["fast reactor", "sodium", "lead-cooled", "mox"],
    "Financing": ["financing", "finance", "investment", "cost"],
    "Delay Risk": ["delay", "licensing", "supply chain", "construction"],
    "Energy Security": ["energy security", "reliability", "coal replacement"],
    "Decarbonization": ["clean", "decarbonization", "emissions", "net zero"],
    "Industrial Heat": ["industrial heat", "hydrogen", "desalination", "process heat", "data center"],
}

def tag_topics(text: str) -> dict[str, int]:
    t = str(text).lower()
    return {topic: int(any(k in t for k in keys)) for topic, keys in TOPICS.items()}
