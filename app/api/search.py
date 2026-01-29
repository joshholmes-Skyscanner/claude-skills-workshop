from fastapi import APIRouter
from app.models import SearchRequest, SearchResponse
from app.services.planner import Planner

router = APIRouter()

@router.post("/search", response_model=SearchResponse)
async def search(req: SearchRequest) -> SearchResponse:
    planner = Planner()
    plans = await planner.search(req)
    return SearchResponse(plans=plans)
