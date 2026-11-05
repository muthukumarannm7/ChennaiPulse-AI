import sqlite3
from pathlib import Path

# Always use the database inside this backend folder
DB_PATH = Path(__file__).resolve().parent / "chennai_pulse.db"

if not DB_PATH.exists():
    raise FileNotFoundError(
        f"Database not found: {DB_PATH}"
    )

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check columns that already exist
cursor.execute("PRAGMA table_info(incidents)")
existing_columns = {
    column[1] for column in cursor.fetchall()
}

# New columns to add
new_columns = {
    "source_report_id": "INTEGER REFERENCES reports(id)",
    "transport_mode": "VARCHAR DEFAULT 'unknown'",
    "sentiment": "VARCHAR DEFAULT 'neutral'",
    "location_confidence": "FLOAT DEFAULT 0.0",
    "duplicate_group": "VARCHAR",
    "priority_level": "VARCHAR DEFAULT 'low'",
    "priority_explanation": "VARCHAR"
}

try:
    for column_name, column_type in new_columns.items():
        if column_name not in existing_columns:
            cursor.execute(
                f"ALTER TABLE incidents ADD COLUMN "
                f"{column_name} {column_type}"
            )
            print(f"Added column: {column_name}")
        else:
            print(f"Already exists: {column_name}")

    conn.commit()
    print("\nDatabase migration completed successfully!")

except Exception as error:
    conn.rollback()
    print(f"\nMigration failed: {error}")
    raise

finally:
    conn.close()