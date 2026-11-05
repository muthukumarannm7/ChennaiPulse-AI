"""Possible duplicate candidate detection. Reports are never merged or deleted."""
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def find_duplicates(incident, existing_reports, threshold=0.35):
    description = str(incident.get("description") or "").strip()
    if not description:
        return []

    new_category = str(
        incident.get("incident_type") or incident.get("category") or ""
    ).strip().lower()
    new_location = str(incident.get("location_name") or "").strip().lower()
    candidates = []

    for report in existing_reports or []:
        old_description = str(report.get("description") or "").strip()
        if not old_description:
            continue

        try:
            matrix = TfidfVectorizer(ngram_range=(1, 2)).fit_transform(
                [description.lower(), old_description.lower()]
            )
            text_score = float(cosine_similarity(matrix[0:1], matrix[1:2])[0][0])
        except ValueError:
            text_score = 0.0

        old_category = str(
            report.get("incident_type") or report.get("category") or ""
        ).strip().lower()
        old_location = str(report.get("location_name") or "").strip().lower()

        category_match = bool(
            new_category and old_category and new_category == old_category
        )
        location_match = bool(
            new_location and old_location and new_location == old_location
        )

        score = (
            0.60 * text_score
            + (0.25 if category_match else 0.0)
            + (0.15 if location_match else 0.0)
        )
        if score >= threshold:
            candidates.append({
                "report_id": report.get("report_id"),
                "duplicate_group": report.get("duplicate_group") or report.get("report_id"),
                "text_similarity": round(text_score, 3),
                "score": round(score, 3),
                "category_match": category_match,
                "location_match": location_match,
            })

    return sorted(candidates, key=lambda item: item["score"], reverse=True)
