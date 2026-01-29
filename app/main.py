from fastapi import FastAPI
from app.api.search import router as search_router

app = FastAPI(title="Orbital Travel Planner", version="0.1.0")

app.include_router(search_router, prefix="/api")

@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
