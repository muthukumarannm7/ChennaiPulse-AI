
from uuid import uuid4

from sqlalchemy.orm import Session

from models import Report, Incident
from ai.extraction import extract_incident
from intelligence import analyze_incident
from intelligence.category import normalize_category


def create_citizen_report(
    report_text: str,
    language: str,
    db: Session
):
    """
    Save the citizen report, run AI extraction and intelligence analysis,
    then save the processed incident.
    """

    report_id = f"RPT-{uuid4().hex[:8].upper()}"

    try:
        # 1. Create the original citizen report.
        new_report = Report(
            report_code=report_id,
            description=report_text,
            language=language
        )

        db.add(new_report)
        db.flush()  # Generates the report ID without committing.

        # 2. Member 2: Extract incident information.
        extracted = extract_incident(
            report_text=report_text,
            language=language
        )

        # 3. Member 3: Prepare existing incidents for duplicate detection.
        existing_incidents = db.query(Incident).all()

        existing_reports = [
            {
                "report_id": str(item.source_report_id or item.id),
                "description": item.description,
                "incident_type": item.incident_type,
                "location_name": item.location_name,
                "duplicate_group": item.duplicate_group
            }
            for item in existing_incidents
        ]

        # 4. Member 3: Run category, location, duplicate and priority analysis.
        intelligence = analyze_incident(
            extracted_data=extracted,
            existing_reports=existing_reports
        )

        # 5. Normalize the category and severity.
        incident_type = normalize_category(
            extracted.get("incident_type"),
            extracted.get("description") or report_text
        )

        severity = str(
            extracted.get("severity") or "medium"
        ).lower()

        if severity not in {"low", "medium", "high", "critical"}:
            severity = "medium"

        # 6. Create the processed incident.
        new_incident = Incident(
            source_report_id=new_report.id,
            incident_type=incident_type,
            description=extracted.get("description") or report_text,
            transport_mode=extracted.get("transport_mode") or "unknown",
            severity=severity,
            sentiment=extracted.get("sentiment") or "neutral",
            processing_method=extracted.get("processing_method") or "rule_based",
            location_name=intelligence.get("location_name"),
            latitude=intelligence.get("latitude"),
            longitude=intelligence.get("longitude"),
            location_confidence=intelligence.get("location_confidence", 0.0),
            duplicate_group=intelligence.get("duplicate_group"),
            priority_score=intelligence.get("priority_score", 0.0),
            priority_level=intelligence.get("priority_level", "low"),
            priority_explanation=intelligence.get("priority_explanation"),
            verification_status="unverified"
        )

        db.add(new_incident)

        # 7. Save both report and incident together.
        db.commit()
        db.refresh(new_report)
        db.refresh(new_incident)

        return {
            "success": True,
            "report_id": report_id,
            "message": "Citizen report processed successfully",
            "incident": new_incident
        }

    except Exception:
        db.rollback()
        raise
