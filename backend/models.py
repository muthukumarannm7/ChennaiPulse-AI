
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey
)
from sqlalchemy.sql import func

from database import Base


# Table 1: Original citizen reports
class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)

    report_code = Column(
        String,
        unique=True,
        index=True
    )

    description = Column(String, nullable=False)

    language = Column(
        String,
        default="English"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )


# Table 2: Processed mobility incidents
class Incident(Base):
    __tablename__ = "incidents"

    id = Column(Integer, primary_key=True, index=True)

    # Link to the original citizen report
    source_report_id = Column(
        Integer,
        ForeignKey("reports.id"),
        nullable=True,
        index=True
    )

    # AI extraction results - Member 2
    incident_type = Column(String, nullable=False)

    description = Column(String, nullable=False)

    transport_mode = Column(
        String,
        default="unknown"
    )

    severity = Column(
        String,
        default="medium"
    )

    sentiment = Column(
        String,
        default="neutral"
    )

    processing_method = Column(
        String,
        default="rule_based"
    )

    # Location intelligence - Member 3
    location_name = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    location_confidence = Column(
        Float,
        default=0.0
    )

    # Duplicate detection - Member 3
    duplicate_group = Column(
        String,
        nullable=True
    )

    # Priority intelligence - Member 3
    priority_score = Column(
        Float,
        default=0.0
    )

    priority_level = Column(
        String,
        default="low"
    )

    priority_explanation = Column(
        String,
        nullable=True
    )

    # Authority verification
    verification_status = Column(
        String,
        default="unverified"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
