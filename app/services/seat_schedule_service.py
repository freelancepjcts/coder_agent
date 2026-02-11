from sqlalchemy.orm import Session
from sqlalchemy import and_, extract, or_
from collections import defaultdict
from datetime import date, time

from app.models.slot_request_daily import SlotRequestsDaily


class SeatScheduleService:

    @staticmethod
    def get_seat_schedule_view(
        db: Session,
        schedule: str | None,
        from_date: date | None,
        to_date: date| None,
        excluding_airline: str | None,
        terminal: str | None,
        days: list[int] | None,
        slot_start: time | None,
        slot_end: time | None,
        hours: int | None
    ):
        q = db.query(SlotRequestsDaily)

        # Date range
        if from_date and to_date:
            q = q.filter(
                SlotRequestsDaily.arrival_date.between(from_date, to_date)
            )

        # Schedule / Season
        if schedule:
            q = q.filter(SlotRequestsDaily.season == schedule)

        # Excluding airline
        if excluding_airline:
            q = q.filter(SlotRequestsDaily.ai_code != excluding_airline)

        # Terminal
        if terminal:
            q = q.filter(SlotRequestsDaily.iata_airport_code == terminal)

        if days:
            if not all(1 <= d <= 7 for d in days):
                raise ValueError("Days must be between 1 and 7")

            q = q.filter(
                extract('isodow', SlotRequestsDaily.arrival_date).in_(days)
            )

        if slot_start and slot_end:

            if slot_start >= slot_end:
                raise ValueError("slot_start must be less than slot_end")

            q = q.filter(
                SlotRequestsDaily.sta_lt >= slot_start,
                SlotRequestsDaily.std_lt <= slot_end
            )

        if hours is not None:
            upper_time = time(hours, 0, 0) 
            q = q.filter(
                or_(
                SlotRequestsDaily.sta_lt < upper_time,
                SlotRequestsDaily.std_lt < upper_time
                )
            )    

        q = q.order_by(SlotRequestsDaily.sta_lt.asc())

        records = q.all()

        arrival = defaultdict(lambda: defaultdict(list))
        departure = defaultdict(lambda: defaultdict(list))

        for r in records:
            day_key = f"Day {r.arrival_date.isoweekday()}"
            
            if r.sta_lt:
                hour = r.sta_lt.hour
                next_hour = (hour + 1) % 24
                slot = f"{hour:02d}:00-{next_hour:02d}:00"
                arrival[day_key][slot].append(r)

            if r.std_lt:
                hour_start = r.std_lt.replace(minute=0, second=0, microsecond=0)                
                hour = hour_start.hour
                prev_hour = (hour - 1) % 24              
                slot = f"{prev_hour:02d}:00-{hour:02d}:00"
                departure[day_key][slot].append(r)



        return {
            "arrival": SeatScheduleService._format(arrival, is_arrival=True),
            "departure": SeatScheduleService._format(departure, is_arrival=False)
        }

    @staticmethod
    def _format(data, is_arrival: bool):
        response = []

        for day, slots in sorted(data.items()):
            slot_list = []

            for slot, flights in sorted(slots.items()):
                slot_list.append({
                    "slot_hours": slot,
                    "total_seat": sum(f.seat for f in flights),
                    "flights": [
                        {
                            "status": f.approval_status,
                            "airline_code": f.ai_code,
                            "flight_no": f.arr_flt if is_arrival else f.dep_flt,
                            "aircraft_code": f.ac_code,
                            "route": f.a_route1 if is_arrival else f.d_route1,
                            "sta": f.sta_lt.strftime("%H:%M") if is_arrival and f.sta_lt else None,
                            "std": f.std_lt.strftime("%H:%M") if not is_arrival and f.std_lt else None,
                            "eff_date": f.arrival_date
                        }
                        for f in flights
                    ]
                })

            response.append({
                "day": day,
                "slots": slot_list
            })

        return response
