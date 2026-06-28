from fastapi import APIRouter
from fastapi import Depends, FastAPI
import app

router = APIRouter()

@router.get("/health")
def health_endpoint():
    """
    Dummy health endpoint for testing purposes.
    """
    return {"message": "Hello World"}