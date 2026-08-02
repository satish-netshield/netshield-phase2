from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"

SEVERITY_POINTS = {
    "Low": 10,
    "Medium": 20,
    "High": 30,
    "Critical": 40,
}

RISK_POINTS = {
    "Low": 10,
    "Medium": 20,
    "High": 30,
    "Critical": 40,
}


def connect_database() -> sqlite3.Connection:
    """Connect to the enterprise database with foreign keys enabled."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def classify_severity(score: int) -> str:
    """Convert a classification score into a final severity."""

    if score <= 20:
        return "Low"

    if score <= 40:
        return "Medium"

    if score <= 60:
        return "High"

    return "Critical"


def classify_incidents() -> None:
    """Classify incidents using initial severity and asset risk."""

    connection = connect_database()

    try:
        incidents = connection.execute(
            """
            SELECT
                incidents.incident_id,
                incidents.incident_type,
                incidents.initial_severity,
                incidents.severity,
                assets.asset_name,
                risk_scores.risk_level
            FROM incidents
            JOIN assets
                ON incidents.asset_id = assets.asset_id
            JOIN risk_scores
                ON incidents.asset_id = risk_scores.asset_id
            ORDER BY incidents.incident_id
            """
        ).fetchall()

        if not incidents:
            print("No incidents found for severity classification.")
            return

        print("\nNetShield Enterprise Severity Classification")
        print("-" * 115)

        for incident in incidents:
            incident_id = incident[0]
            incident_type = incident[1]
            initial_severity = incident[2]
            previous_severity = incident[3]
            asset_name = incident[4]
            asset_risk = incident[5]

            initial_points = SEVERITY_POINTS.get(initial_severity, 0)
            risk_points = RISK_POINTS.get(asset_risk, 0)
            classification_score = initial_points + risk_points
            final_severity = classify_severity(classification_score)

            classification_reason = (
                f"Initial severity: {initial_severity} "
                f"({initial_points} points); "
                f"asset risk: {asset_risk} "
                f"({risk_points} points); "
                f"classification score: {classification_score}; "
                f"final severity: {final_severity}"
            )

            connection.execute(
                """
                UPDATE incidents
                SET
                    severity = ?,
                    classification_reason = ?
                WHERE incident_id = ?
                """,
                (
                    final_severity,
                    classification_reason,
                    incident_id,
                ),
            )

            print(
                f"ID: {incident_id} | "
                f"Asset: {asset_name} | "
                f"Incident: {incident_type} | "
                f"Initial: {initial_severity} | "
                f"Asset Risk: {asset_risk} | "
                f"Score: {classification_score} | "
                f"Final: {final_severity}"
            )

            if previous_severity != final_severity:
                print(
                    f"  Severity updated: "
                    f"{previous_severity} -> {final_severity}"
                )
            else:
                print("  Severity unchanged.")

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Severity classification failed: {error}")
        raise

    finally:
        connection.close()


def list_classified_incidents() -> None:
    """Display incidents after severity classification."""

    connection = connect_database()

    try:
        incidents = connection.execute(
            """
            SELECT
                incident_id,
                incident_type,
                initial_severity,
                severity,
                classification_reason
            FROM incidents
            ORDER BY incident_id
            """
        ).fetchall()

        print("\nClassified Incident Results")
        print("-" * 115)

        for incident in incidents:
            print(
                f"ID: {incident[0]} | "
                f"Type: {incident[1]} | "
                f"Initial: {incident[2]} | "
                f"Final: {incident[3]}"
            )
            print(f"  Reason: {incident[4]}")

    finally:
        connection.close()


if __name__ == "__main__":
    classify_incidents()
    list_classified_incidents()
