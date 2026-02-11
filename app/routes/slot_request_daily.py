from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.seat_schedule_request import SeatScheduleRequest
from app.schemas.slot_requests_daily_response import SlotRequestsDailyResponse
from app.services.seat_schedule_service import SeatScheduleService
from app.services.slot_request_daily_service import create_slot_request_daily, get_by_airport
from app.services.airport_service import get_airport_by_iata
from app.schemas.response import ApiResponse
from datetime import date, time
from typing import List, Optional

router = APIRouter()

@router.post(
    "/slot-requests-daily",
    response_model=ApiResponse[SlotRequestsDailyResponse],
    status_code=201
)
def create_slot_request(
    payload: dict,
    db: Session = Depends(get_db)
):
    slot = create_slot_request_daily(db, payload)

    return ApiResponse(
        message="Slot request daily created successfully",
        data=SlotRequestsDailyResponse.model_validate(slot)
    )

@router.get(
    "/slot-requests-daily/airport",
    response_model=ApiResponse[dict]
)
def search_by_airport(
    airport_code:  Optional[str] = Query("", max_length=10),
    limit: int = Query(50, ge=1, le=500),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    if airport_code is not None and airport_code != "":
        airport = get_airport_by_iata(db, airport_code)
        airport_name = airport.full_name if airport else None
    else:
        airport_name = "All Airports"

    results = get_by_airport(
        db=db,
        airport_code=airport_code, #airport null check will happen inside the service function
        limit=limit,
        offset=offset
    )

    response_items = [
        SlotRequestsDailyResponse.model_validate(slot)
        for slot in results
    ]

    return ApiResponse(
        message="Slot request daily search results",
        data={"airport_name": airport_name, "results": response_items}
    )


@router.post("/seat-schedules/view")
def seat_schedule_view(
    request: SeatScheduleRequest,
    db: Session = Depends(get_db)
):
    return SeatScheduleService.get_seat_schedule_view(
        db=db,
        schedule=request.schedule,
        from_date=request.from_date,
        to_date=request.to_date,
        excluding_airline=request.excluding_airline,
        terminal=request.terminal,
        days=request.days,
        slot_start=request.slot_start,
        slot_end=request.slot_end,
        hours = request.hours
    )