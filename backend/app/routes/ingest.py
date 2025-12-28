from fastapi import APIRouter
from pydantic import BaseModel, Field
from app.services.feature_engineering import update_features

router = APIRouter()

class TransactionEvent(BaseModel):
    event_id: str
    user_id: str
    amount: float
    currency: str = "INR"
    merchant_id: str
    merchant_category: str = "OTHER"
    lat: float
    lon: float
    ts: str = Field(..., description="ISO timestamp, e.g. 2025-12-27T12:00:00Z")

@router.post("/ingest")
def ingest(evt: TransactionEvent):
    features = update_features(evt.model_dump())
    return {"ok": True, "features": features}