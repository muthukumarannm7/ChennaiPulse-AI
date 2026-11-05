
from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime


# Citizen complaint submission
class ReportCreate(BaseModel):
    text: str = Field(
        min_length=5,
        max_length=2000,
        description="Citizen's original mobility complaint"
    )

    language: str = Field(
        default="English",
        description="Language used in the complaint"
    )


# Processed incident response
class IncidentResponse(BaseModel):
    id: int
    source_report_id: Optional[int] = None

    # AI extraction results - Member 2
    incident_type: str
    description: str
    transport_mode: str = "unknown"
    severity: str
    sentiment: str = "neutral"
    processing_method: str

    # Location intelligence - Member 3
    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    location_confidence: float = 0.0

    # Duplicate detection
    duplicate_group: Optional[str] = None

    # Priority intelligence
    priority_score: float
    priority_level: str = "low"
    priority_explanation: Optional[str] = None

    # Authority verification
    verification_status: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


# Report submission response
class ReportResponse(BaseModel):
    success: bool
    report_id: str
    message: str
    incident: Optional[IncidentResponse] = None


# Incident verification status update
class IncidentStatusUpdate(BaseModel):
    verification_status: Literal[
        "unverified",
        "verified",
        "rejected",
        "resolved"
    ]
