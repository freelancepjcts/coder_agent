# app/routes/slot_details.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.slot_detail_service import SlotDetailsService

router = APIRouter()

@router.get("/slot-details")
def get_slot_details(page: int = 1, db: Session = Depends(get_db)):
    service = SlotDetailsService(db)
    return service.get_slot_details(page)
