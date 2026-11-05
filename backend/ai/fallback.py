"""Rule-based fallback for ChennaiPulse AI incident extraction."""
import re

INCIDENT_TYPES = {
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

KEYWORDS = {
    "bus_breakdown": [
        "bus breakdown", "bus broke down", "bus has broken down",
        "பேருந்து பழுத", "பஸ் பழுத", "பேருந்து நின்று",
    ],
    "traffic_congestion": [
        "traffic", "traffic jam", "congestion", "heavy traffic",
        "நெரிசல்", "போக்குவரத்து நெரிசல்", "வாகன நெரிசல்",
    ],
    "road_accident": ["accident", "crash", "collision", "விபத்து"],
    "waterlogging": [
        "waterlogging", "water logging", "flood", "water stagnation",
        "மழைநீர் தேங்க", "தண்ணீர் தேங்க", "வெள்ளம்",
    ],
    "road_damage": [
        "pothole", "damaged road", "road damage", "broken road",
        "சாலை சேதம்", "குண்டும் குழியும",
    ],
    "signal_malfunction": [
        "signal not working", "signal failure", "traffic signal",
        "signal malfunction", "சிக்னல் வேலை செய்யவில்லை",
        "போக்குவரத்து சிக்னல்",
    ],
    "public_transport_disruption": [
        "metro delay", "train delay", "bus service cancelled",
        "service disruption", "ரயில் தாமதம்", "மெட்ரோ தாமதம்",
    ],
    "footpath_accessibility": [
        "footpath blocked", "footpath inaccessible", "sidewalk blocked",
        "நடைபாதை",
    ],
    "parking_issue": [
        "illegal parking", "no parking", "parking issue", "wrong parking",
    ],
}

# These aliases extract a locality name only. Coordinates are resolved by Member 3.
BUILTIN_LOCALITIES = {
    "anna nagar": "Anna Nagar",
    "அண்ணா நகர்": "Anna Nagar",
    "saidapet": "Saidapet",
    "சைதாப்பேட்டை": "Saidapet",
    "guindy": "Guindy",
    "கிண்டி": "Guindy",
    "t nagar": "T Nagar",
    "டி நகர்": "T Nagar",
    "தியாகராய நகர்": "T Nagar",
    "velachery": "Velachery",
    "வேளச்சேரி": "Velachery",
    "adyar": "Adyar",
    "அடையாறு": "Adyar",
    "tambaram": "Tambaram",
    "தாம்பரம்": "Tambaram",
    "porur": "Porur",
    "போரூர்": "Porur",
}


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _detect_language(text: str, requested: str) -> str:
    if re.search(r"[\u0B80-\u0BFF]", text):
        return "Tamil"

    padded = f" {_normalise(text)} "
    tanglish_terms = (" la ", " irukku", " aayiduchu", " nikkuthu", " romba ")
    if any(term in padded for term in tanglish_terms):
        return "Tanglish"

    if requested and requested.strip().lower() not in {"", "auto", "unknown"}:
        return requested.strip()

    return "English"


def _find_category(text: str) -> str:
    normal = _normalise(text)
    for category, phrases in KEYWORDS.items():
        if any(_normalise(phrase) in normal for phrase in phrases):
            return category
    return "other"


def _find_location(text: str):
    normal = _normalise(text)
    for raw, canonical in sorted(
        BUILTIN_LOCALITIES.items(),
        key=lambda item: len(item[0]),
        reverse=True,
    ):
        pattern = rf"(?<![a-z0-9]){re.escape(raw)}(?![a-z0-9])"
        if re.search(pattern, normal):
            return canonical
    return None


def _find_transport(text: str, category: str) -> str:
    normal = _normalise(text)
    terms = [
        (["bus", "பேருந்து", "பஸ்"], "bus"),
        (["metro", "மெட்ரோ"], "metro"),
        (["train", "ரயில்"], "train"),
        (["bike", "motorcycle", "scooter"], "bike"),
        (["car", "கார்"], "car"),
    ]

    for keywords, mode in terms:
        if any(keyword in normal for keyword in keywords):
            return mode

    if category in {
        "traffic_congestion", "road_accident", "road_damage",
        "waterlogging", "signal_malfunction", "parking_issue",
    }:
        return "road"

    return "unknown"


def _severity(text: str, category: str) -> str:
    normal = _normalise(text)

    if any(term in normal for term in [
        "heavy", "severe", "major", "blocked", "emergency",
        "கடுமையான", "பெரிய விபத்து",
    ]):
        return "high"

    if any(term in normal for term in ["minor", "slight", "சிறிய"]):
        return "low"

    if category == "road_accident":
        return "high"

    return "unknown" if category == "other" else "medium"


def fallback_extract(report_text: str, language: str = "English") -> dict:
    """Return the same eight-field contract as extract_incident()."""
    if not isinstance(report_text, str) or not report_text.strip():
        raise ValueError("report_text must be a non-empty string")

    category = _find_category(report_text)
    return {
        "incident_type": category,
        "description": report_text.strip(),
        "location_name": _find_location(report_text),
        "transport_mode": _find_transport(report_text, category),
        "severity": _severity(report_text, category),
        "sentiment": "negative",
        "language": _detect_language(report_text, language),
        "processing_method": "rule_based",
    }
