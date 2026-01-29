import pytest
import respx
from httpx import Response
from datetime import datetime, timezone, timedelta

from app.main import app
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_search_returns_plans_with_valid_shape(monkeypatch):
    # Mock MCP routes.get so tests are deterministic without running docker.
    with respx.mock(assert_all_called=True) as rsps:
        rsps.post("http://localhost:8765/tools/routes.get").respond(
            200,
            json={
                "itineraries": [
                    {"legs": [{"origin":"LON","destination":"NYC","mode":"flight","provider":"earth-air","duration_minutes":450}]},
                    {"legs": [
                        {"origin":"LON","destination":"KEF","mode":"flight","provider":"earth-air","duration_minutes":180},
                        {"origin":"KEF","destination":"NYC","mode":"flight","provider":"northwind","duration_minutes":360},
                    ]},
                ]
            },
        )

        req = {
            "origin":"LON",
            "destination":"NYC",
            "depart_after": datetime.now(timezone.utc).isoformat(),
            "arrive_before": (datetime.now(timezone.utc) + timedelta(days=2)).isoformat(),
            "max_layovers": 2,
            "optimize_for":"balanced",
        }

        async with AsyncClient(app=app, base_url="http://test") as client:
            r = await client.post("/api/search", json=req)
            assert r.status_code == 200
            data = r.json()
            assert "plans" in data
            assert len(data["plans"]) >= 1
            plan0 = data["plans"][0]
            assert plan0["metrics"]["total_price_gbp"] >= 0
            assert 0 <= plan0["metrics"]["risk_score"] <= 1
