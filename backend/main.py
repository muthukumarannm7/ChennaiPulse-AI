from fastapi import FastAPI

app = FastAPI(
    title="ChennaiPulse AI",
    description="Citizen-powered mobility intelligence platform",
    version="1.0.0"
)

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