from fastapi import APIRouter, HTTPException
from app.services.feature_engineering import get_features
from app.services.risk_scoring import compute_risk_score

router = APIRouter()

@router.get("/score/{user_id}")
def score_user(user_id: str):
    features = get_features(user_id)
    if not features:
        raise HTTPException(status_code=404, detail="User not found")

    risk = compute_risk_score(features)

    return {
        "user_id": user_id,
        "risk_score": risk,
        "features": features
    }
