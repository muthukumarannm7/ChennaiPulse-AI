
from sqlalchemy import Column, Integer, String, Float, DateTime
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

    incident_type = Column(String, nullable=False)

    description = Column(String, nullable=False)

    location_name = Column(String, nullable=True)

    latitude = Column(Float, nullable=True)

    longitude = Column(Float, nullable=True)

    severity = Column(String, default="medium")

    priority_score = Column(Float, default=0)

    verification_status = Column(
        String,
        default="unverified"
    )

    processing_method = Column(
        String,
        default="rule_based"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
