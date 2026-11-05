
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Incident
from schemas import IncidentStatusUpdate

router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


# Get all incidents
@router.get("/")
def get_incidents(db: Session = Depends(get_db)):

    incidents = db.query(Incident).order_by(
        Incident.id.desc()
    ).all()

    return incidents


# Get one incident by ID
@router.get("/{incident_id}")
def get_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


# Update incident verification status
@router.patch("/{incident_id}/status")
def update_incident_status(
    incident_id: int,
    status_data: IncidentStatusUpdate,
    db: Session = Depends(get_db)
):

    incident = db.query(Incident).filter(
        Incident.id == incident_id
    ).first()

    if incident is None:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    incident.verification_status = (
        status_data.verification_status
    )

    db.commit()
    db.refresh(incident)

    return {
        "success": True,
        "message": "Incident status updated",
        "incident_id": incident.id,
        "verification_status": incident.verification_status
    }
