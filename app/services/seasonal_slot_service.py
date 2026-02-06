from datetime import datetime
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models.slot_request_seasonal import SlotRequestsSeasonal

class SeasonalSlotService:

    @staticmethod
    def create(db: Session, data: dict):

        arrival = data["arrival"]
        departure = data["departure"]

        schedule = SlotRequestsSeasonal(

            # system fields
            conversation_id=data["conversation_id"],
            message_id=data["message_id"],
            senders_email="system@api",
            senders_subject="Seasonal Schedule Creation",

            kuwait_local_airway=True,
            season="SUMMER",
            date_of_message=datetime.utcnow().date(),

            iata_airport_code="KWI",
            action_code="NEW",

            # period
            sfrom=data["fromDate"],
            still=data["toDate"],

            # aircraft
            ai_code=data["airlineCode"],
            ac_code=data["aircraftType"],
            reg="TBD",
            seat=180,

            # flights
            arr_flt=arrival["flightNumber"],
            dep_flt=departure["flightNumber"],

            # routes
            a_route1=arrival["routes"][0]["origin"],
            d_route1=departure["routes"][0]["destination"],

                
            # days
            arr_days=",".join(map(str, arrival["arrivalDays"])),
            dep_days=",".join(map(str, departure["departureDays"])),

            arrival_service_code=arrival["serviceCode"],
            departure_service_code=departure["serviceCode"],

            # times (UTC)
            sta=arrival["sta"],
            std=departure["std"],

            eta=arrival["eta"],
            etd=departure["etd"],

            ata=arrival["ata"],
            atd=departure["atd"],

            # local times
            sta_lt=arrival["sta_lt"],
            std_lt=departure["std_lt"],

            sta_request=arrival["sta_request"],
            std_request=departure["std_request"],

            overnight_indicator=data["overnight_indicator"],

            # nature
            arr_natu=arrival["arrivalNature"],
            dep_natu=departure["departureNature"],
            arr_natu_full=arrival["arrivalNature"],
            dep_natu_full=departure["departureNature"],

            approval_status=data["approval"],
            flag_for_review=False,
            ref=data["ref"],
            last_update=data["last_update"],
            ac_body_type="NARROW"
        )

        db.add(schedule)
        db.commit()
        db.refresh(schedule)

        return schedule

    @staticmethod
    def get_by_id(db: Session, schedule_id: int):

        schedule = (
            db.query(SlotRequestsSeasonal)
            .filter(SlotRequestsSeasonal.id == schedule_id)
            .first()
        )

        if not schedule:
            raise HTTPException(status_code=404, detail="Schedule not found")

        return {
            "id": schedule.id,
            "conversation_id": schedule.conversation_id,
            "message_id": schedule.message_id,
            "airline_code": schedule.ai_code,
            "aircraft_type": schedule.ac_code,
            "period": {
                "from": schedule.sfrom,
                "to": schedule.still
            },
            "arrival": {
                "flight": schedule.arr_flt,
                "route": schedule.a_route1,
                "days": schedule.arr_days,
                "sta": schedule.sta_lt,
                "gate": schedule.arr_skd_gate
            },
            "departure": {
                "flight": schedule.dep_flt,
                "route": schedule.d_route1,
                "days": schedule.dep_days,
                "std": schedule.std_lt,
                "gate": schedule.dep_skd_gate
            },
            "approval_status": schedule.approval_status,
            "last_update": schedule.last_update
        }
