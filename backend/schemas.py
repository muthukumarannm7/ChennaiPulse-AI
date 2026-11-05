
from pydantic import BaseModel, Field
from typing import Optional


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
    incident_type: str
    description: str

    location_name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    severity: str
    priority_score: float

    verification_status: str
    processing_method: str

    class Config:
        from_attributes = True


# Report submission response
class ReportResponse(BaseModel):
    success: bool
    report_id: str
    message: str
    incident: Optional[IncidentResponse] = None
