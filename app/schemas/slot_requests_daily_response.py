from pydantic import BaseModel
from datetime import date, datetime, time
from typing import Optional


class SlotRequestsDailyResponse(BaseModel):
    id: int

    conversation_id: str
    message_id: str

    senders_email: str
    senders_subject: str

    kuwait_local_airway: bool

    season: str
    date_of_message: date

    iata_airport_code: str
    action_code: str

    arrival_date: date
    departure_date: date

    from_operation_period: Optional[date] = None
    till_operation_period: Optional[date] = None

    ai_code: str
    reg: str
    ac_code: str
    calls: Optional[str] = None
    seat: int

    arr_flt: str
    dep_flt: str

    a_route1: str
    d_route1: str

    a_route2: Optional[str] = None
    d_route2: Optional[str] = None

    a_route3: Optional[str] = None
    d_route3: Optional[str] = None

    a_route4: Optional[str] = None
    d_route4: Optional[str] = None

    arr_days: str
    dep_days: str

    sta: datetime
    eta: datetime
    ata: datetime

    std: datetime
    etd: datetime
    atd: datetime

    sta_lt: time
    std_lt: time

    sta_request: Optional[time] = None
    std_request: Optional[time] = None

    arr_skd_gate: Optional[str] = None
    dep_skd_gate: Optional[str] = None

    overnight_indicator: int

    arrival_service_code: str
    departure_service_code: str

    arr_natu: str
    dep_natu: str

    arr_natu_full: str
    dep_natu_full: str

    remarks: Optional[str] = None
    remarks_for_review: Optional[str] = None

    flag_for_review: bool

    approval_status: str

    ref: datetime
    last_update: datetime

    ac_body_type: str

    class Config:
        from_attributes = True  # SQLAlchemy ORM support
