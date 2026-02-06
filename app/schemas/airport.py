from pydantic import BaseModel
from typing import Optional


class AirportResponse(BaseModel):
    iata_code: str
    full_name: str
    full_name_arabic: Optional[str] = None
    country: str
    country_arabic: Optional[str] = None

    class Config:
        from_attributes = True
