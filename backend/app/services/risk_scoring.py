import math

def compute_risk_score(features: dict) -> float:
    """
    Combines behavior features into a normalized risk score in [0,1]
    """

    velocity = features.get("txn_count_10m", 0)
    geo_jump = features.get("geo_jump_km", 0.0)
    merchant_risk = features.get("merchant_risk_avg", 0.0)
    avg_amount = features.get("avg_amount_1h", 0.0)

    # Normalize components
    velocity_score = min(velocity / 10, 1)
    geo_score = min(geo_jump / 500, 1)
    merchant_score = merchant_risk
    amount_score = min(math.log1p(avg_amount) / 10, 1)

    risk = (
        0.35 * velocity_score +
        0.25 * geo_score +
        0.25 * merchant_score +
        0.15 * amount_score
    )

    return round(min(risk, 1.0), 3)
