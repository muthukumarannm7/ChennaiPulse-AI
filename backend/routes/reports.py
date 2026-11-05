
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Report
from schemas import ReportCreate, ReportResponse
from services.report_service import create_citizen_report

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
        result = create_citizen_report(
            report_text=report_data.text,
            language=report_data.language,
            db=db
        )

        return {
            **result,
            "incident": None
        }

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Unable to process the citizen report"
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
