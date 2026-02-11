from datetime import date, time
from typing import Optional, List
from pydantic import BaseModel

class SeatScheduleRequest(BaseModel):
    schedule: Optional[str] = None
    from_date: date = None
    to_date: date = None
    excluding_airline: Optional[str] = None
    terminal: Optional[str] = None

    # Slot hours
    slot_start: Optional[time] = None
    slot_end: Optional[time] = None

    # Days Applicable: 1=Mon ... 7=Sun
    days: Optional[List[int]] = None
    hours: int = None