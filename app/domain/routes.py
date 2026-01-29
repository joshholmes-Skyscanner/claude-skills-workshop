from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass(frozen=True)
class RouteEdge:
    origin: str
    destination: str
    mode: str          # flight | orbital
    provider: str
    duration_minutes: int

def estimate_times(
    depart_after: datetime,
    duration_minutes: int,
) -> tuple[datetime, datetime]:
    depart_at = depart_after
    arrive_at = depart_after + timedelta(minutes=duration_minutes)
    return depart_at, arrive_at
