from __future__ import annotations

def estimate_emissions_kg(mode: str, duration_minutes: int) -> float:
    # intentionally rough; orbital is "worse" for fun.
    if mode == "orbital":
        return round(5.0 * (duration_minutes / 60.0), 3)
    return round(1.2 * (duration_minutes / 60.0), 3)
