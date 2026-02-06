# app/services/slot_details_service.py
from math import ceil
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.orm import Session

class SlotDetailsService:
    PAGE_SIZE = 2

    STATUS_META = {
        "Open": {"color": "#f9735b", "accent": "#ffe2da"},
        "Confirm": {"color": "#48c78e", "accent": "#dff7ed"},
        "Offer": {"color": "#ffb347", "accent": "#ffe9d5"},
        "Pending": {"color": "#4c6ef5", "accent": "#e3e9ff"},
        "Holding": {"color": "#a855f7", "accent": "#f3e4ff"},
        "Refusal": {"color": "#f06292", "accent": "#ffe2ec"},
        "Cancellation": {"color": "#94a3b8", "accent": "#edf0f5"},
    }

    def __init__(self, db: Session):
        self.db = db

    # ---------- Summary and Chart ----------
    def get_summary_and_chart(self):
        query = text("""
            SELECT approval_status, COUNT(*) AS count
            FROM slot_requests_daily
            GROUP BY approval_status
        """)

        rows = self.db.execute(query).mappings().all()
        total = sum(r["count"] for r in rows)

        summary = []
        chart = []

        for r in rows:
            status = r["approval_status"]
            count = r["count"]
            meta = self.STATUS_META.get(status, {"color": "#999", "accent": "#eee"})
            percent = round((count / total) * 100) if total else 0

            summary.append({
                "key": status,
                "title": status,
                "count": count,
                "color": meta["color"],
                "accent": meta["accent"]
            })

            chart.append({
                "name": status,
                "value": count,
                "color": meta["color"],
                "percent": percent
            })

        return summary, chart

    # ---------- PAGINATED SLOTS ----------
    def get_slots(self, page: int = 1):
        offset = (page - 1) * self.PAGE_SIZE

        data_query = text("""
            SELECT
                id,
                date_of_message AS date,
                TO_CHAR(date_of_message, 'DD.MM.YYYY') AS "displayDate",
                senders_email AS email,
                remarks,
                approval_status AS status,
                ref AS "createdAt",
                last_update AS "updatedAt"
            FROM slot_requests_daily
            ORDER BY id ASC
            LIMIT :limit OFFSET :offset
        """)

        rows = self.db.execute(
            data_query,
            {"limit": self.PAGE_SIZE, "offset": offset}
        ).mappings().all()

        items = []
        for r in rows:
            status = r["status"]
            items.append({
                "id": r["id"],
                "date": r["date"],
                "displayDate": r["displayDate"],
                "email": r["email"],
                "remarks": r["remarks"],
                "user": {
                    "id": "",
                    "name": ""
                },
                "status": status,
                "statusColor": self.STATUS_META.get(status, {}).get("color", "#999999"),
                "createdAt": r["createdAt"].isoformat() if r["createdAt"] else None,
                "updatedAt": r["updatedAt"].isoformat() if r["updatedAt"] else None
            })

        count_query = text("SELECT COUNT(*) FROM slot_requests_daily")
        total_items = self.db.execute(count_query).scalar()

        return items, total_items

    # ---------- FINAL RESPONSE ----------
    def get_slot_details(self, page: int = 1):
        summary, chart = self.get_summary_and_chart()
        items, total_items = self.get_slots(page)

        total_pages = ceil(total_items / self.PAGE_SIZE)

        return {
            "summary": summary,
            "chart": chart,
            "slots": {
                "items": items,
                "pagination": {
                    "page": page,
                    "pageSize": self.PAGE_SIZE,
                    "totalItems": total_items,
                    "totalPages": total_pages
                }
            },
            "meta": {
                "generatedAt": datetime.now(timezone.utc).isoformat(),
                "timezone": "UTC"
            }
        }
