# ChennaiPulse AI — Member 2: AI Extraction

Included:
- backend/ai/extraction.py
- backend/ai/fallback.py
- backend/ai/__init__.py
- requirements-member2-member3.txt

Copy the `backend/ai/` folder into the matching location in the project.
Install dependencies with:
`pip install -r requirements-member2-member3.txt`

Ollama is optional. If enabled, pull the model with:
`ollama pull qwen2.5:3b`

Test from the backend directory:
`python -c "from ai.extraction import extract_incident; print(extract_incident('Heavy traffic near Anna Nagar'))"`

Output contract: incident_type, description, location_name, transport_mode, severity, sentiment, language, processing_method.
