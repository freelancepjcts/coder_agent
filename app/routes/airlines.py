from fastapi import APIRouter
from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
import app
from app.db.session import get_db
from app.models.model import Airline

router = APIRouter()

@router.get("/airlines")
def get_airlines(db: Session = Depends(get_db)):
    return db.query(Airline).all()