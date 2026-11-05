
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from uuid import uuid4

from database import get_db
from models import Report
from schemas import ReportCreate, ReportResponse

router = APIRouter(
    prefix="/api/reports",
    tags=["Reports"]
)


@router.post("/", response_model=ReportResponse)
def create_report(
    report_data: ReportCreate,
    db: Session = Depends(get_db)
):
    try:
        # Generate a unique report ID
        report_id = f"RPT-{uuid4().hex[:8].upper()}"

        # Create database record
        new_report = Report(
            report_code=report_id,
            description=report_data.text,
            language=report_data.language
        )

        # Save report
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return {
            "success": True,
            "report_id": report_id,
            "message": "Citizen report submitted successfully",
            "incident": None
        }

    except Exception as error:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Unable to save the report"
        )
        

@router.get("/")
def get_reports(db: Session = Depends(get_db)):
    reports = db.query(Report).order_by(
        Report.id.desc()
    ).all()

    return [
        {
            "report_id": report.report_code,
            "description": report.description,
            "language": report.language,
            "created_at": report.created_at
        }
        for report in reports
    ]
