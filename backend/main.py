
from fastapi import FastAPI

# Database imports
from database import engine, Base
import models

# API router imports
from routes.reports import router as reports_router
from routes.incidents import router as incidents_router


# Create database tables automatically
Base.metadata.create_all(bind=engine)


# Initialize FastAPI application
app = FastAPI(
    title="ChennaiPulse AI",
    description="Citizen-powered mobility intelligence platform for Chennai",
    version="1.0.0"
)


# Register API routers
app.include_router(reports_router)
app.include_router(incidents_router)


# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to ChennaiPulse AI Backend!",
        "status": "Running",
        "project": "Citizen-powered mobility intelligence platform"
    }


# Health check endpoint
@app.get("/api/health")
def health():
    return {
        "status": "healthy",
        "application": "ChennaiPulse AI"
    }


# Database connection check
@app.get("/api/database")
def database_status():
    return {
        "database": "SQLite",
        "status": "connected",
        "tables": ["reports", "incidents"]
    }
