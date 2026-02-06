from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    DateTime,
    Time,
    Text
)
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class SlotRequestsDaily(Base):
    __tablename__ = "slot_requests_daily"

    id = Column(Integer, primary_key=True, index=True)

    conversation_id = Column(String(255), nullable=False)
    message_id = Column(String(255), nullable=False)

    senders_email = Column(String(255), nullable=False)
    senders_subject = Column(String(500), nullable=False)

    kuwait_local_airway = Column(Boolean, nullable=False)

    season = Column(String(50), nullable=False)
    date_of_message = Column(Date, nullable=False)

    iata_airport_code = Column(String(10), nullable=False)
    action_code = Column(String(50), nullable=False)

    arrival_date = Column(Date, nullable=False)
    departure_date = Column(Date, nullable=False)

    from_operation_period = Column(Date, nullable=True)
    till_operation_period = Column(Date, nullable=True)

    ai_code = Column(String(10), nullable=False)
    reg = Column(String(20), nullable=False)
    ac_code = Column(String(20), nullable=False)
    calls = Column(String(20), nullable=True)
    seat = Column(Integer, nullable=False)

    arr_flt = Column(String(50), nullable=False)
    dep_flt = Column(String(50), nullable=False)

    a_route1 = Column(String(10), nullable=False)
    d_route1 = Column(String(10), nullable=False)

    a_route2 = Column(String(10), nullable=True)
    d_route2 = Column(String(10), nullable=True)

    a_route3 = Column(String(10), nullable=True)
    d_route3 = Column(String(10), nullable=True)

    a_route4 = Column(String(10), nullable=True)
    d_route4 = Column(String(10), nullable=True)

    arr_days = Column(String(50), nullable=False)
    dep_days = Column(String(50), nullable=False)

    sta = Column(DateTime, nullable=False)
    eta = Column(DateTime, nullable=False)
    ata = Column(DateTime, nullable=False)

    std = Column(DateTime, nullable=False)
    etd = Column(DateTime, nullable=False)
    atd = Column(DateTime, nullable=False)

    sta_lt = Column(Time, nullable=False)
    std_lt = Column(Time, nullable=False)

    sta_request = Column(Time, nullable=True)
    std_request = Column(Time, nullable=True)

    arr_skd_gate = Column(String(20), nullable=True)
    dep_skd_gate = Column(String(20), nullable=True)

    overnight_indicator = Column(Integer, nullable=False)

    arrival_service_code = Column(String(50), nullable=False)
    departure_service_code = Column(String(50), nullable=False)

    arr_natu = Column(String(50), nullable=False)
    dep_natu = Column(String(50), nullable=False)

    arr_natu_full = Column(String(100), nullable=False)
    dep_natu_full = Column(String(100), nullable=False)

    remarks = Column(Text, nullable=True)
    remarks_for_review = Column(Text, nullable=True)

    flag_for_review = Column(Boolean, default=False)

    approval_status = Column(String(50), nullable=False)

    ref = Column(DateTime, nullable=False)
    last_update = Column(DateTime, nullable=False)

    ac_body_type = Column(String(50), nullable=False)
