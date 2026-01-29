import pytest
from app.services.validator import validate_plan, ValidationError
from app.models import Plan, Leg, PlanMetrics
from datetime import datetime, timezone

def test_validator_rejects_negative_price():
    plan = Plan(
        legs=[Leg(provider="x", mode="flight", origin="AAA", destination="BBB",
                  depart_at=datetime.now(timezone.utc), arrive_at=datetime.now(timezone.utc),
                  duration_minutes=10)],
        layovers=0,
        metrics=PlanMetrics(total_price_gbp=-1, total_duration_minutes=10, total_emissions_kg=0.1, risk_score=0.1),
        score=0.0,
        explanation="x",
    )
    with pytest.raises(ValidationError):
        validate_plan(plan)

@pytest.mark.xfail(reason="Workshop: add stronger invariant checks (time windows, layovers, ordering)")
def test_validator_rejects_inconsistent_times():
    # TODO in workshop: validate monotonic leg times + layover windows.
    assert False
