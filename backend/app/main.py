from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.health import router as health_router
from app.routes.ingest import router as ingest_router
from app.routes.score import router as score_router

app = FastAPI(title="Risk Feature Store")

# 👇 ADD THIS BLOCK
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # allow requests from frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router)
app.include_router(ingest_router)
app.include_router(score_router)
