from __future__ import annotations

import os
import random
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="Workshop MCP Server", version="0.1.0")

CHAOS = os.environ.get("MCP_CHAOS", "0") == "1"

class RoutesRequest(BaseModel):
    origin: str = Field(min_length=3, max_length=3)
    destination: str = Field(min_length=3, max_length=3)
    max_layovers: int = Field(default=2, ge=0, le=6)

@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True, "chaos": CHAOS}

@app.post("/tools/routes.get")
def routes_get(req: RoutesRequest) -> dict:
    # Deterministic-ish sample itineraries (replace with real provider simulation later)
    base = [
        # direct-ish flight
        {"legs": [{"origin": req.origin, "destination": req.destination, "mode": "flight", "provider": "earth-air", "duration_minutes": 450}]},
        # one stop
        {"legs": [
            {"origin": req.origin, "destination": "KEF", "mode": "flight", "provider": "earth-air", "duration_minutes": 180},
            {"origin": "KEF", "destination": req.destination, "mode": "flight", "provider": "northwind", "duration_minutes": 360},
        ]},
        # silly orbital transfer (fun route)
        {"legs": [
            {"origin": req.origin, "destination": "ISS", "mode": "orbital", "provider": "orbitalx", "duration_minutes": 90},
            {"origin": "ISS", "destination": req.destination, "mode": "flight", "provider": "earth-air", "duration_minutes": 420},
        ]},
        # longer but "green-ish" (pretend)
        {"legs": [
            {"origin": req.origin, "destination": "AMS", "mode": "flight", "provider": "tulip", "duration_minutes": 80},
            {"origin": "AMS", "destination": req.destination, "mode": "flight", "provider": "tulip", "duration_minutes": 420},
        ]},
    ]

    # respect max_layovers
    itins = [i for i in base if (len(i["legs"]) - 1) <= req.max_layovers]

    if CHAOS:
        rnd = random.random()
        if rnd < 0.15:
            raise HTTPException(status_code=500, detail="provider timeout")
        if rnd < 0.30:
            # partial data
            itins = itins[:2]
        if rnd < 0.40:
            random.shuffle(itins)

    return {"itineraries": itins}

def main() -> None:
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("MCP_PORT", "8765")))

if __name__ == "__main__":
    main()
