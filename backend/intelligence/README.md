# ChennaiPulse AI — Member 3: Intelligence Engine

Included:
- backend/intelligence/__init__.py
- category.py, location.py, duplicate.py, priority.py
- data/locations.csv (71 locality records)
- requirements-member2-member3.txt

Copy `backend/intelligence/` into the matching project folder and replace the project's `data/locations.csv` with the included file.
Install dependencies with:
`pip install -r requirements-member2-member3.txt`

Test from the backend directory:
`python -c "from intelligence import analyze_incident; print(analyze_incident({'incident_type':'traffic_congestion','description':'Heavy traffic near Anna Nagar','location_name':'Anna Nagar','severity':'high'}, []))"`

The CSV columns are name,aliases,latitude,longitude. The 71 coordinates are representative locality-centre references, not exact incident locations or surveyed boundaries. Verify them against a trusted mapping source before production use. If a locality is not matched or coordinates are invalid, the resolver returns null coordinates and confidence 0.0.

Output contract: location_name, latitude, longitude, location_confidence, duplicate_group, priority_score, priority_level, priority_explanation.

Duplicate detection identifies possible candidates only; it does not merge or delete incidents.
