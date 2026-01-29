from app.services.planner import Planner
from app.models import PlanMetrics, OptimizeFor

def test_scoring_orders_reasonably():
    p = Planner()
    m1 = PlanMetrics(total_price_gbp=100, total_duration_minutes=300, total_emissions_kg=5, risk_score=0.2)
    m2 = PlanMetrics(total_price_gbp=200, total_duration_minutes=200, total_emissions_kg=4, risk_score=0.2)

    assert p._score(m1, OptimizeFor.cheapest) > p._score(m2, OptimizeFor.cheapest)
    assert p._score(m2, OptimizeFor.fastest) > p._score(m1, OptimizeFor.fastest)
