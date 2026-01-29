from __future__ import annotations

from app.models import Plan

class ValidationError(Exception):
    pass

def validate_plan(plan: Plan) -> None:
    if plan.metrics.total_price_gbp < 0:
        raise ValidationError("negative price")
    if plan.layovers != max(0, len(plan.legs) - 1):
        raise ValidationError("layover count mismatch")
    if plan.metrics.risk_score < 0 or plan.metrics.risk_score > 1:
        raise ValidationError("risk_score out of range")
