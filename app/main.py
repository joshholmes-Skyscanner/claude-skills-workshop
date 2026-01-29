from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
from app.api.search import router as search_router

app = FastAPI(title="Orbital Travel Planner", version="0.1.0")

app.include_router(search_router, prefix="/api")

# Serve static files (frontend)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

    @app.get("/")
    def root() -> FileResponse:
        return FileResponse(static_dir / "index.html")

@app.get("/healthz")
def healthz() -> dict:
    return {"ok": True}
