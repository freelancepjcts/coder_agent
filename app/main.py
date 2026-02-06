from fastapi import FastAPI
from app.routes import airlines, seasonal_slots, slot_details, slot_request_daily

app = FastAPI(title="My App")

# Global API prefix
app.include_router(airlines.router, prefix="/api")
app.include_router(seasonal_slots.router, prefix="/api") #schedules
app.include_router(slot_request_daily.router, prefix="/api") #sector schedules
app.include_router(slot_details.router, prefix="/api") #flights