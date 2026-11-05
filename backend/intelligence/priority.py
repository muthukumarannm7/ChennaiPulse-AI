"""Transparent, configurable first-pass incident priority scoring."""

CATEGORY_POINTS = {
    "road_accident": 25,
    "waterlogging": 20,
    "road_blockage": 20,
    "signal_malfunction": 15,
    "bus_breakdown": 15,
    "traffic_congestion": 15,
    "public_transport_disruption": 15,
    "road_damage": 10,
    "footpath_accessibility": 8,
    "parking_issue": 5,
    "other": 5,
}

SEVERITY_POINTS = {
    "critical": 60,
    "high": 45,
    "medium": 30,
    "low": 15,
}


def calculate_priority(incident, category=None, location_confidence=0.0):
    severity = str(incident.get("severity") or "medium").strip().lower()
    incident_category = str(
        category
        or incident.get("incident_type")
        or incident.get("category")
        or "other"
    ).strip().lower()

    severity_points = SEVERITY_POINTS.get(severity, SEVERITY_POINTS["medium"])
    category_points = CATEGORY_POINTS.get(incident_category, CATEGORY_POINTS["other"])

    try:
        confidence = max(0.0, min(float(location_confidence), 1.0))
    except (TypeError, ValueError):
        confidence = 0.0

    score = round(
        min(100.0, severity_points + category_points + (15.0 * confidence)),
        2,
    )

    if score >= 80:
        level = "critical"
    elif score >= 60:
        level = "high"
    elif score >= 40:
        level = "medium"
    else:
        level = "low"

    explanation = (
        f"{severity.capitalize()} severity {incident_category.replace('_', ' ')}; "
        f"severity points={severity_points}, category points={category_points}, "
        f"location confidence={confidence:.2f}; total={score}/100."
    )

    return {
        "priority_score": score,
        "priority_level": level,
        "priority_explanation": explanation,
    }
