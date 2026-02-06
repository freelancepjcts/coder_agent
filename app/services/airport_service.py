from sqlalchemy.orm import Session
from app.models.airport import Airport


def get_airport_by_iata(
    db: Session,
    iata_code: str
):
    return (
        db.query(Airport)
        .filter(Airport.iata_code == iata_code)
        .first()
    )
