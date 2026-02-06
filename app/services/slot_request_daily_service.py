from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.models.slot_request_daily import SlotRequestsDaily



def create_slot_request_daily(
    db: Session,
    payload: dict
) -> SlotRequestsDaily:
    data = {
        "conversation_id": payload.get("conversation_id"),
        "message_id": payload.get("message_id"),

        "senders_email": payload.get("senders_email"),
        "senders_subject": payload.get("senders_subject"),

        "kuwait_local_airway": payload.get("kuwait_local_airway"),

        "season": payload.get("season"),
        "date_of_message": payload.get("date_of_message"),

        "iata_airport_code": payload.get("iata_airport_code"),
        "action_code": payload.get("action_code"),

        "arrival_date": payload.get("arrival_date"),
        "departure_date": payload.get("departure_date"),

        "from_operation_period": payload.get("from_operation_period"),
        "till_operation_period": payload.get("till_operation_period"),

        "ai_code": payload.get("ai_code"),
        "reg": payload.get("reg"),
        "ac_code": payload.get("ac_code"),
        "calls": payload.get("calls"),
        "seat": payload.get("seat"),

        "arr_flt": payload.get("arr_flt"),
        "dep_flt": payload.get("dep_flt"),

        "a_route1": payload.get("a_route1"),
        "d_route1": payload.get("d_route1"),

        "a_route2": payload.get("a_route2"),
        "d_route2": payload.get("d_route2"),

        "a_route3": payload.get("a_route3"),
        "d_route3": payload.get("d_route3"),

        "a_route4": payload.get("a_route4"),
        "d_route4": payload.get("d_route4"),

        "arr_days": payload.get("arr_days"),
        "dep_days": payload.get("dep_days"),

        "sta": payload.get("sta"),
        "eta": payload.get("eta"),
        "ata": payload.get("ata"),

        "std": payload.get("std"),
        "etd": payload.get("etd"),
        "atd": payload.get("atd"),

        "sta_lt": payload.get("sta_lt"),
        "std_lt": payload.get("std_lt"),

        "sta_request": payload.get("sta_request"),
        "std_request": payload.get("std_request"),

        "arr_skd_gate": payload.get("arr_skd_gate"),
        "dep_skd_gate": payload.get("dep_skd_gate"),

        "overnight_indicator": payload.get("overnight_indicator"),

        "arrival_service_code": payload.get("arrival_service_code"),
        "departure_service_code": payload.get("departure_service_code"),

        "arr_natu": payload.get("arr_natu"),
        "dep_natu": payload.get("dep_natu"),

        "arr_natu_full": payload.get("arr_natu_full"),
        "dep_natu_full": payload.get("dep_natu_full"),

        "remarks": payload.get("remarks"),
        "remarks_for_review": payload.get("remarks_for_review"),

        "flag_for_review": payload.get("flag_for_review", False),

        "approval_status": payload.get("approval_status"),

        "ref": payload.get("ref"),
        "last_update": payload.get("last_update"),

        "ac_body_type": payload.get("ac_body_type")
    }

    slot = SlotRequestsDaily(**data)

    db.add(slot)
    db.commit()
    db.refresh(slot)

    return slot

def get_by_airport(
    db: Session,
    airport_code: str,
    limit: int,
    offset: int
):
    query = db.query(SlotRequestsDaily)
    if airport_code is not None and airport_code != "":
     query = query.filter(
        or_(
            SlotRequestsDaily.a_route1 == airport_code,
            SlotRequestsDaily.d_route1 == airport_code
        )
    )

    return (
        query
        .order_by(SlotRequestsDaily.date_of_message.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
