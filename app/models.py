from __future__ import annotations

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field

class OptimizeFor(str, Enum):
    cheapest = "cheapest"
    fastest = "fastest"
    greenest = "greenest"
    balanced = "balanced"

class SearchRequest(BaseModel):
    origin: str = Field(min_length=3, max_length=3, description="IATA-ish code, e.g. LON")
    destination: str = Field(min_length=3, max_length=3, description="IATA-ish code, e.g. NYC")
    depart_after: datetime
    arrive_before: datetime
    max_layovers: int = Field(default=2, ge=0, le=6)
    optimize_for: OptimizeFor = OptimizeFor.balanced

class Leg(BaseModel):
    provider: str
    mode: str  # flight | orbital
    origin: str
    destination: str
    depart_at: datetime
    arrive_at: datetime
    duration_minutes: int

class PlanMetrics(BaseModel):
    total_price_gbp: float
    total_duration_minutes: int
    total_emissions_kg: float
    risk_score: float  # 0..1

class Plan(BaseModel):
    legs: list[Leg]
    layovers: int
    metrics: PlanMetrics
    score: float
    explanation: str

class SearchResponse(BaseModel):
    plans: list[Plan]
