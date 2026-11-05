"""Category normalization for the ChennaiPulse intelligence engine."""

STANDARD_CATEGORIES = {
    "bus_breakdown",
    "traffic_congestion",
    "road_accident",
    "waterlogging",
    "road_damage",
    "signal_malfunction",
    "public_transport_disruption",
    "footpath_accessibility",
    "parking_issue",
    "other",
}

ALIASES = {
    "bus_breakdown": [
        "bus breakdown", "bus stopped", "bus not working",
        "bus failure", "bus problem",
    ],
    "traffic_congestion": [
        "traffic", "traffic jam", "heavy traffic",
        "traffic congestion", "vehicles stuck",
    ],
    "road_accident": ["accident", "road accident", "vehicle collision", "crash"],
    "waterlogging": [
        "waterlogging", "flooded road", "road flooded",
        "rain water", "water on road",
    ],
    "road_damage": ["pothole", "damaged road", "broken road", "road damage"],
    "signal_malfunction": [
        "signal malfunction", "traffic signal not working",
        "signal not working", "broken signal",
    ],
    "public_transport_disruption": [
        "metro delay", "train delay", "bus delay", "transport delay",
        "public transport disruption", "metro service disruption",
    ],
    "footpath_accessibility": [
        "blocked footpath", "damaged footpath",
        "footpath accessibility", "footpath blocked",
    ],
    "parking_issue": [
        "illegal parking", "parking issue", "vehicle parked", "no parking",
    ],
}


def normalize_category(value, description="") -> str:
    """Return one of the ten agreed category names."""
    raw = str(value or "").strip().lower()
    if raw in STANDARD_CATEGORIES:
        return raw

    combined = f"{raw} {str(description or '').lower()}".strip()
    matches = []
    for category, phrases in ALIASES.items():
        for phrase in phrases:
            if phrase in combined:
                matches.append((len(phrase), category))

    if matches:
        return max(matches)[1]
    return "other"
