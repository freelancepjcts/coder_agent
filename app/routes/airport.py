from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from app.schemas.airport import AirportResponse
from app.schemas.response import ApiResponse
from services.airport_service import search_airports

router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)


@router.get(
    "/search",
    response_model=ApiResponse[List[AirportResponse]]
)
def search_airport(
    keyword: str = Query(..., min_length=2),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    results = search_airports(
        db=db,
        keyword=keyword,
        limit=limit,
        offset=offset
    )

    return ApiResponse(
        message="Airport search results",
        data=results
    )
