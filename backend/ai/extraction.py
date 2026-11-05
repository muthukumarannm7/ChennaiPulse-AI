"""Ollama/Qwen incident extraction with rule-based fallback."""
import json
import os

import requests

from .fallback import fallback_extract

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5:3b")

ALLOWED_TYPES = {
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

REQUIRED_KEYS = {
    "incident_type",
    "description",
    "location_name",
    "transport_mode",
    "severity",
    "sentiment",
    "language",
    "processing_method",
}


def _prompt(report_text: str, language: str) -> str:
    return f"""
Extract the mobility incident. Understand English, Tamil and Tanglish.
Return only JSON with exactly these keys: {sorted(REQUIRED_KEYS)}
incident_type must be one of: {sorted(ALLOWED_TYPES)}
location_name must be explicitly mentioned or null. Never invent it.
Do not return coordinates, geocoding or duplicate information.
transport_mode: bus, metro, train, bike, car, road, unknown.
severity: low, medium, high, unknown.
sentiment: positive, neutral, negative.
language: English, Tamil, Tanglish, Tamil-English.
processing_method: ollama.
Keep description in the original language.
Language hint: {language}
Complaint: {report_text}
""".strip()


def _validate(data: dict, report_text: str, language: str) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Model response is not a JSON object")

    result = {key: data.get(key) for key in REQUIRED_KEYS}

    if result["incident_type"] not in ALLOWED_TYPES:
        result["incident_type"] = "other"

    if not isinstance(result["description"], str) or not result["description"].strip():
        result["description"] = report_text.strip()

    if result["location_name"] is not None and not isinstance(result["location_name"], str):
        result["location_name"] = None

    if result["transport_mode"] not in {
        "bus", "metro", "train", "bike", "car", "road", "unknown"
    }:
        result["transport_mode"] = "unknown"

    if result["severity"] not in {"low", "medium", "high", "unknown"}:
        result["severity"] = "unknown"

    if result["sentiment"] not in {"positive", "neutral", "negative"}:
        result["sentiment"] = "negative"

    allowed_languages = {"English", "Tamil", "Tanglish", "Tamil-English"}
    if result["language"] not in allowed_languages:
        result["language"] = language if language in allowed_languages else "English"

    result["processing_method"] = "ollama"
    return result


def extract_incident(report_text: str, language: str = "English") -> dict:
    """Extract incident fields; use deterministic fallback if Ollama is unavailable."""
    if not isinstance(report_text, str) or not report_text.strip():
        raise ValueError("report_text must be a non-empty string")

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": OLLAMA_MODEL,
                "prompt": _prompt(report_text, language),
                "stream": False,
                "format": "json",
                "options": {"temperature": 0},
            },
            timeout=25,
        )
        response.raise_for_status()
        payload = response.json()
        return _validate(
            json.loads(payload.get("response", "")),
            report_text,
            language,
        )
    except (
        requests.RequestException,
        ValueError,
        TypeError,
        KeyError,
        json.JSONDecodeError,
    ):
        return fallback_extract(report_text, language)
