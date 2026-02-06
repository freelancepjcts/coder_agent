from sqlalchemy import (
    Column, String, Integer, Boolean,
    Date, DateTime, Time, Text
)
from app.db.base import Base


class SlotRequestsSeasonal(Base):
    __tablename__ = "slot_requests_seasonal"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(String(255))
    message_id = Column(String(255))

    senders_email = Column(String(255))
    senders_subject = Column(String(500))

    kuwait_local_airway = Column(Boolean)

    season = Column(String(50))
    date_of_message = Column(Date)

    iata_airport_code = Column(String(10))
    action_code = Column(String(50))

    sfrom = Column(Date)
    still = Column(Date)

    ai_code = Column(String(10))
    reg = Column(String(20))
    ac_code = Column(String(20))
    calls = Column(String(20), nullable=True)
    seat = Column(Integer)

    arr_flt = Column(String(50))
    dep_flt = Column(String(50))

    a_route1 = Column(String(10))
    d_route1 = Column(String(10))

    a_route2 = Column(String(10), nullable=True)
    d_route2 = Column(String(10), nullable=True)

    a_route3 = Column(String(10), nullable=True)
    d_route3 = Column(String(10), nullable=True)

    a_route4 = Column(String(10), nullable=True)
    d_route4 = Column(String(10), nullable=True)

    arr_days = Column(String(50))
    dep_days = Column(String(50))

    sta = Column(DateTime)
    eta = Column(DateTime)
    ata = Column(DateTime)

    std = Column(DateTime)
    etd = Column(DateTime)
    atd = Column(DateTime)

    sta_lt = Column(Time)
    std_lt = Column(Time)

    sta_request = Column(Time)
    std_request = Column(Time)

    arr_skd_gate = Column(String(20), nullable=True)
    dep_skd_gate = Column(String(20), nullable=True)

    overnight_indicator = Column(Integer)

    arrival_service_code = Column(String(50))
    departure_service_code = Column(String(50))

    arr_natu = Column(String(50))
    dep_natu = Column(String(50))

    arr_natu_full = Column(String(100))
    dep_natu_full = Column(String(100))

    remarks = Column(Text, nullable=True)
    remarks_for_review = Column(Text, nullable=True)

    flag_for_review = Column(Boolean, default=False)

    approval_status = Column(String(50))

    ref = Column(DateTime)
    last_update = Column(DateTime)

    ac_body_type = Column(String(50))
