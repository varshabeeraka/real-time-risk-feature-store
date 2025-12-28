from __future__ import annotations
from datetime import datetime, timedelta, timezone
from typing import Dict, List, Tuple, Any
import math

_STORE: Dict[str, Dict[str, Any]] = {}

MERCHANT_RISK = {
    "GROCERY": 0.10,
    "FUEL": 0.25,
    "ECOMMERCE": 0.45,
    "TRAVEL": 0.55,
    "JEWELRY": 0.75,
    "GAMBLING": 0.90,
    "OTHER": 0.35,
}

def _parse_ts(ts: str) -> datetime:
    if ts.endswith("Z"):
        ts = ts[:-1] + "+00:00"
    return datetime.fromisoformat(ts).astimezone(timezone.utc)

def _haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dlon / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))

def update_features(event: dict) -> dict:
    user_id = event["user_id"]
    amount = float(event["amount"])
    category = (event.get("merchant_category") or "OTHER").upper()
    lat = float(event["lat"])
    lon = float(event["lon"])
    ts = _parse_ts(event["ts"])

    rec = _STORE.get(user_id) or {
        "user_id": user_id,
        "updated_at": ts.isoformat(),
        "history": [],  # (ts_iso, amount, lat, lon, category)
        "txn_count_10m": 0,
        "avg_amount_1h": 0.0,
        "sum_amount_24h": 0.0,
        "geo_jump_km": 0.0,
        "merchant_risk_avg": 0.0,
    }

    history: List[Tuple[str, float, float, float, str]] = rec["history"]

    # geo jump vs last txn
    if history:
        _, _, last_lat, last_lon, _ = history[-1]
        rec["geo_jump_km"] = _haversine_km(last_lat, last_lon, lat, lon)
    else:
        rec["geo_jump_km"] = 0.0

    history.append((ts.isoformat(), amount, lat, lon, category))
    if len(history) > 300:
        history[:] = history[-300:]

    t10 = ts - timedelta(minutes=10)
    t1h = ts - timedelta(hours=1)
    t24 = ts - timedelta(hours=24)

    cnt_10m = 0
    sum_1h = 0.0
    cnt_1h = 0
    sum_24 = 0.0
    risk_sum_24 = 0.0
    risk_cnt_24 = 0

    for ts_iso, amt, _, _, hcat in history:
        hts = _parse_ts(ts_iso)
        if hts >= t10:
            cnt_10m += 1
        if hts >= t1h:
            sum_1h += amt
            cnt_1h += 1
        if hts >= t24:
            sum_24 += amt
            risk_sum_24 += MERCHANT_RISK.get(hcat, MERCHANT_RISK["OTHER"])
            risk_cnt_24 += 1

    rec["txn_count_10m"] = cnt_10m
    rec["avg_amount_1h"] = (sum_1h / cnt_1h) if cnt_1h else 0.0
    rec["sum_amount_24h"] = sum_24
    rec["merchant_risk_avg"] = (risk_sum_24 / risk_cnt_24) if risk_cnt_24 else 0.0
    rec["updated_at"] = ts.isoformat()

    _STORE[user_id] = rec
    return {k: v for k, v in rec.items() if k != "history"}

def get_features(user_id: str) -> dict | None:
    rec = _STORE.get(user_id)
    if not rec:
        return None
    return {k: v for k, v in rec.items() if k != "history"}