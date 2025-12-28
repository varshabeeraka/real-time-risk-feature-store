Real-Time Credit Risk Feature Engineering & Scoring System

This project simulates how modern banks and fintech companies generate real-time behavioral risk features and compute fraud / credit risk scores before approving transactions or loans.

It converts raw transaction events into meaningful behavioral intelligence using rolling time windows, geo-anomaly detection, and merchant risk profiling, and exposes a low-latency risk scoring API with a live React dashboard.

Architecture
Transaction Event
      |
      v
   POST /ingest  (FastAPI)
      |
      v
Feature Engineering Engine
(velocity, geo jump, rolling spend, merchant risk)
      |
      v
 In-Memory Feature Store
      |
      v
 GET /score/{user_id}
      |
      v
React Risk Dashboard

Tech Stack
Layer	Technology
Backend	Python, FastAPI
Frontend	React
Storage	In-memory (AWS DynamoDB ready)
Features	Rolling window feature engineering
Scoring	Weighted fraud & credit risk model

Features Generated
Feature	Description
txn_count_10m	Number of transactions in last 10 minutes
avg_amount_1h	Average spend in last 1 hour
sum_amount_24h	Total spend in last 24 hours
geo_jump_km	Distance between last and current transaction
merchant_risk_avg	Average merchant category risk in last 24 hours

Run Backend Locally
venv\Scripts\activate
cd backend
uvicorn app.main:app --reload

Ingest Sample Transactions
Invoke-RestMethod -Method Post http://127.0.0.1:8000/ingest `
  -ContentType "application/json" `
  -Body '{
    "event_id": "e1",
    "user_id": "U123",
    "amount": 1500,
    "currency": "INR",
    "merchant_id": "M55",
    "merchant_category": "GROCERY",
    "lat": 12.9716,
    "lon": 77.5946,
    "ts": "2025-12-27T12:00:00Z"
  }'

Get Risk Score
Invoke-RestMethod http://127.0.0.1:8000/score/U123

Run Frontend
cd frontend
npm start

http://localhost:3000
