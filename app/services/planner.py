from __future__ import annotations

from datetime import timedelta

from app.models import SearchRequest, Plan, Leg, PlanMetrics, OptimizeFor
from app.domain.routes import estimate_times
from app.domain.pricing import base_price_gbp, apply_modifiers
from app.domain.emissions import estimate_emissions_kg
from app.domain.risk import estimate_risk_score
from app.services.validator import validate_plan
from app.services.mcp_client import MCPClient


class Planner:
    """Naive planner.

    Workshop goal: replace with graph search, provider data via MCP, and better scoring.
    """

    def __init__(self) -> None:
        self.mcp = MCPClient()

    async def search(self, req: SearchRequest) -> list[Plan]:
        # provider routes (mock)
        routes = await self.mcp.call("routes.get", {
            "origin": req.origin,
            "destination": req.destination,
            "max_layovers": req.max_layovers,
        })

        # naive: pick first 3 candidate itineraries from provider
        candidates = routes.get("itineraries", [])[:3]
        plans: list[Plan] = []
        for itin in candidates:
            legs: list[Leg] = []
            t = req.depart_after
            total_duration = 0
            total_price = 0.0
            total_emissions = 0.0
            worst_risk = 0.0

            for seg in itin["legs"]:
                duration = int(seg["duration_minutes"])
                depart_at, arrive_at = estimate_times(t, duration)
                leg = Leg(
                    provider=seg["provider"],
                    mode=seg["mode"],
                    origin=seg["origin"],
                    destination=seg["destination"],
                    depart_at=depart_at,
                    arrive_at=arrive_at,
                    duration_minutes=duration,
                )
                legs.append(leg)
                t = arrive_at + timedelta(minutes=35)  # fixed transfer time (intentionally naive)
                total_duration += duration + 35

                risk = estimate_risk_score(seg["provider"], seg["mode"])
                worst_risk = max(worst_risk, risk)

                price = base_price_gbp(seg["mode"], duration)
                price = apply_modifiers(price, peak=False, risk_score=risk)
                total_price += price

                total_emissions += estimate_emissions_kg(seg["mode"], duration)

            if legs and legs[-1].arrive_at > req.arrive_before:
                # discard if too late
                continue

            metrics = PlanMetrics(
                total_price_gbp=round(total_price, 2),
                total_duration_minutes=int(total_duration),
                total_emissions_kg=round(total_emissions, 3),
                risk_score=float(worst_risk),
            )

            score = self._score(metrics, req.optimize_for)
            explanation = self._explain(metrics, req.optimize_for)

            plan = Plan(
                legs=legs,
                layovers=max(0, len(legs) - 1),
                metrics=metrics,
                score=score,
                explanation=explanation,
            )
            validate_plan(plan)
            plans.append(plan)

        # higher score is better (we'll keep it simple for now)
        plans.sort(key=lambda p: p.score, reverse=True)
        return plans

    def _score(self, m: PlanMetrics, optimize_for: OptimizeFor) -> float:
        # naive scoring. Workshop will replace with calibrated model.
        # normalize-ish
        cost = max(m.total_price_gbp, 1.0)
        dur = max(m.total_duration_minutes, 1)
        emi = max(m.total_emissions_kg, 0.001)
        risk = max(m.risk_score, 0.001)

        if optimize_for == OptimizeFor.cheapest:
            return 1.0 / cost
        if optimize_for == OptimizeFor.fastest:
            return 1.0 / dur
        if optimize_for == OptimizeFor.greenest:
            return 1.0 / emi
        # balanced
        return (1.0 / cost) * 0.45 + (1.0 / dur) * 0.35 + (1.0 / emi) * 0.15 + (1.0 / (1.0 + risk)) * 0.05

    def _explain(self, m: PlanMetrics, optimize_for: OptimizeFor) -> str:
        return (
            f"Optimized for {optimize_for.value}. "
            f"Price £{m.total_price_gbp}, duration {m.total_duration_minutes}m, "
            f"emissions {m.total_emissions_kg}kg, risk {m.risk_score}."
        )
