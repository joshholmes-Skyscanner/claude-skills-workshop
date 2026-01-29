from __future__ import annotations
import random

def estimate_risk_score(provider: str, mode: str) -> float:
    # deterministic-ish risk based on provider name; workshop will replace with MCP "space weather".
    seed = sum(ord(c) for c in (provider + mode))
    rnd = random.Random(seed)
    return round(0.15 + rnd.random() * 0.35, 3)  # 0.15..0.5
