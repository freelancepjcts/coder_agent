from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.db.session import Base

class Airline(Base):
    __tablename__ = "airlines"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(10), nullable=False)
    description = Column(String(300))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
