"""Combined intelligence pipeline for ChennaiPulse AI."""
from .category import normalize_category
from .location import resolve_location
from .duplicate import find_duplicates
from .priority import calculate_priority


def analyze_incident(extracted_data: dict, existing_reports: list | None = None) -> dict:
    """
    Enrich Member 2 extraction with locality coordinates, duplicate candidate
    grouping and a transparent priority score.

    Returns the eight intelligence fields expected by the backend.
    """
    if not isinstance(extracted_data, dict):
        raise TypeError("extracted_data must be a dictionary")

    description = str(extracted_data.get("description") or "").strip()
    incident_type = normalize_category(
        extracted_data.get("incident_type"),
        description,
    )

    # Resolve only the locality Member 2 explicitly extracted.
    location = resolve_location(extracted_data.get("location_name") or "")

    normalized_incident = {
        "incident_type": incident_type,
        "description": description,
        "location_name": location["location_name"],
        "severity": extracted_data.get("severity") or "medium",
    }

    # Existing reports should be dictionaries with description, incident_type,
    # location_name, report_id and optionally duplicate_group.
    duplicate_candidates = find_duplicates(
        normalized_incident,
        existing_reports or [],
    )
    duplicate_group = None
    if duplicate_candidates:
        duplicate_group = (
            duplicate_candidates[0].get("duplicate_group")
            or duplicate_candidates[0].get("report_id")
        )

    priority = calculate_priority(
        normalized_incident,
        category=incident_type,
        location_confidence=location["location_confidence"],
    )

    return {
        "location_name": location["location_name"],
        "latitude": location["latitude"],
        "longitude": location["longitude"],
        "location_confidence": location["location_confidence"],
        "duplicate_group": duplicate_group,
        "priority_score": priority["priority_score"],
        "priority_level": priority["priority_level"],
        "priority_explanation": priority["priority_explanation"],
    }


__all__ = ["analyze_incident"]
