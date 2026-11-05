
from sqlalchemy.orm import Session
from uuid import uuid4

from models import Report


def create_citizen_report(
    report_text: str,
    language: str,
    db: Session
):
    """
    Save the original citizen complaint
    in the SQLite database.
    """

    report_id = f"RPT-{uuid4().hex[:8].upper()}"

    new_report = Report(
        report_code=report_id,
        description=report_text,
        language=language
    )

    try:
        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return {
            "success": True,
            "report_id": report_id,
            "message": "Citizen report submitted successfully"
        }

    except Exception:
        db.rollback()
        raise
