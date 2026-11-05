
from fastapi import FastAPI

from database import engine, Base
import models

from routes.reports import router as reports_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ChennaiPulse AI",
    description="Citizen-powered mobility intelligence platform",
    version="1.0.0"
)

app.include_router(reports_router)


@app.get("/")
def home():
    return {
        "message": "Welcome to ChennaiPulse AI Backend!",
        "status": "Running"
    }


@app.get("/api/health")
def health():
    return {
        "status": "healthy"
    }


@app.get("/api/database")
def database_status():
    return {
        "database": "SQLite",
        "status": "connected",
        "tables": ["reports", "incidents"]
    }
