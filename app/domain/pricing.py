from __future__ import annotations

def base_price_gbp(mode: str, duration_minutes: int) -> float:
    # intentionally simplistic; workshop will replace with provider quotes + modifiers
    if mode == "orbital":
        return 500.0 + 8.0 * duration_minutes
    return 40.0 + 0.25 * duration_minutes

def apply_modifiers(price: float, *, peak: bool, risk_score: float) -> float:
    if peak:
        price *= 1.15
    price *= (1.0 + 0.2 * risk_score)
    return round(price, 2)
