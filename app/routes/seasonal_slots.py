from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.response import ApiResponse
from app.schemas.response import ApiResponse
from app.schemas.slot_requests_daily_response import SlotRequestsDailyResponse
from app.services.slot_request_daily_service import create_slot_request_daily
from app.services.seasonal_slot_service import SeasonalSlotService

router = APIRouter()

@router.post("/schedules")
def create_schedule(payload: dict, db: Session = Depends(get_db)):
    schedule = SeasonalSlotService.create(db, payload)
    return {
        "id": schedule.id,
        "message": "Seasonal schedule created successfully"
    }

@router.get("/schedules/{id}")
def get_schedule(id: int, db: Session = Depends(get_db)):
    return SeasonalSlotService.get_by_id(db, id)
