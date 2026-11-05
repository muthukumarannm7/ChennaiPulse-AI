"""Exact-alias Chennai locality resolver. Coordinates are read from data/locations.csv."""
from pathlib import Path
import csv
import re

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CSV_PATH = PROJECT_ROOT / "data" / "locations.csv"


def _clean(value):
    return re.sub(r"\s+", " ", str(value or "").strip().lower())


def load_locations(csv_path=None):
    path = Path(csv_path) if csv_path else DEFAULT_CSV_PATH
    lookup = {}
    if not path.exists():
        return lookup

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"name", "aliases", "latitude", "longitude"}
        if not reader.fieldnames or not required.issubset(set(reader.fieldnames)):
            raise ValueError(
                "locations.csv must contain columns: name,aliases,latitude,longitude"
            )

        for row in reader:
            name = str(row.get("name") or "").strip()
            if not name:
                continue

            aliases = [name]
            aliases.extend(str(row.get("aliases") or "").split("|"))
            for alias in aliases:
                key = _clean(alias)
                if key:
                    lookup[key] = {
                        "name": name,
                        "latitude": row.get("latitude"),
                        "longitude": row.get("longitude"),
                    }
    return lookup


def resolve_location(text, csv_path=None):
    """Resolve an exact locality/alias mentioned; never guess coordinates."""
    lookup = load_locations(csv_path)
    normalized_text = _clean(text)

    empty_result = {
        "location_name": None,
        "latitude": None,
        "longitude": None,
        "location_confidence": 0.0,
    }
    if not normalized_text or not lookup:
        return empty_result

    matches = []
    for alias, record in lookup.items():
        # Latin aliases get word boundaries; Tamil aliases use exact substring matching.
        if re.search(r"[a-z0-9]", alias):
            pattern = rf"(?<![a-z0-9]){re.escape(alias)}(?![a-z0-9])"
            matched = re.search(pattern, normalized_text) is not None
        else:
            matched = alias in normalized_text

        if matched:
            matches.append((len(alias), alias, record))

    if not matches:
        return empty_result

    _, _, best = max(matches, key=lambda item: item[0])
    try:
        latitude = float(best["latitude"])
        longitude = float(best["longitude"])
        if not (-90 <= latitude <= 90 and -180 <= longitude <= 180):
            raise ValueError("Coordinates out of range")
    except (TypeError, ValueError):
        latitude = longitude = None

    if latitude is None or longitude is None:
        return {
            "location_name": best["name"],
            "latitude": None,
            "longitude": None,
            "location_confidence": 0.0,
        }

    # Exact locality match confidence, not a statistical probability.
    return {
        "location_name": best["name"],
        "latitude": latitude,
        "longitude": longitude,
        "location_confidence": 1.0,
    }
