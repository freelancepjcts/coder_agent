from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Airport(Base):
    __tablename__ = "airports"

    iata_code = Column(String(10), primary_key=True, index=True)
    full_name = Column(String(255), nullable=False)
    full_name_arabic = Column(String(255), nullable=True)
    country = Column(String(100), nullable=False)
    country_arabic = Column(String(100), nullable=True)
