from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"


def create_database() -> None:
    """Create the NetShield Enterprise database and required tables."""

    DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS assets (
                asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT NOT NULL,
                asset_type TEXT NOT NULL,
                department TEXT NOT NULL,
                owner TEXT,
                operating_system TEXT,
                ip_address TEXT UNIQUE,
                criticality TEXT NOT NULL
                    CHECK (criticality IN ('Low', 'Medium', 'High', 'Critical')),
                status TEXT NOT NULL DEFAULT 'Active'
                    CHECK (status IN ('Active', 'Inactive', 'Maintenance')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                vulnerability_id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER NOT NULL,
                vulnerability_name TEXT NOT NULL,
                cve_id TEXT,
                severity TEXT NOT NULL
                    CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
                description TEXT,
                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (status IN ('Open', 'In Progress', 'Resolved')),
                discovered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                resolved_at TEXT,
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS incidents (
                incident_id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER NOT NULL,
                incident_type TEXT NOT NULL,
                source_ip TEXT,
                description TEXT NOT NULL,
                severity TEXT NOT NULL
                    CHECK (severity IN ('Low', 'Medium', 'High', 'Critical')),
                status TEXT NOT NULL DEFAULT 'Open'
                    CHECK (
                        status IN (
                            'Open',
                            'Investigating',
                            'Contained',
                            'Resolved'
                        )
                    ),
                detected_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS risk_scores (
                risk_id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_id INTEGER NOT NULL,
                risk_score INTEGER NOT NULL CHECK (risk_score BETWEEN 0 AND 100),
                risk_level TEXT NOT NULL
                    CHECK (risk_level IN ('Low', 'Medium', 'High', 'Critical')),
                calculation_reason TEXT NOT NULL,
                calculated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (asset_id) REFERENCES assets(asset_id)
            )
            """
        )

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS incident_timeline (
                timeline_id INTEGER PRIMARY KEY AUTOINCREMENT,
                incident_id INTEGER NOT NULL,
                event_type TEXT NOT NULL,
                event_description TEXT NOT NULL,
                event_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (incident_id) REFERENCES incidents(incident_id)
            )
            """
        )

        connection.commit()

        print("NetShield Enterprise database created successfully.")
        print(f"Database location: {DATABASE_PATH}")
        print("Tables created:")
        print("- assets")
        print("- vulnerabilities")
        print("- incidents")
        print("- risk_scores")
        print("- incident_timeline")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Database creation failed: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    create_database()
