from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"

ASSET_POINTS = {
    "Low": 10,
    "Medium": 20,
    "High": 30,
    "Critical": 40,
}

SEVERITY_POINTS = {
    "Low": 5,
    "Medium": 10,
    "High": 20,
    "Critical": 30,
}

VULNERABILITY_COUNT_POINTS = 5


def connect_database() -> sqlite3.Connection:
    """Connect to the enterprise database with foreign keys enabled."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def calculate_risk_level(score: int) -> str:
    """Convert a numeric risk score into a risk level."""

    if score <= 20:
        return "Low"

    if score <= 40:
        return "Medium"

    if score <= 60:
        return "High"

    return "Critical"


def get_highest_severity(severity_score: int) -> str:
    """Return the severity label associated with a severity score."""

    for severity, points in SEVERITY_POINTS.items():
        if points == severity_score:
            return severity

    return "None"


def calculate_risk_scores() -> None:
    """Calculate and store a risk score for every enterprise asset."""

    connection = connect_database()

    try:
        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                assets.asset_id,
                assets.asset_name,
                assets.criticality,
                COUNT(vulnerabilities.vulnerability_id),
                MAX(
                    CASE vulnerabilities.severity
                        WHEN 'Critical' THEN 30
                        WHEN 'High' THEN 20
                        WHEN 'Medium' THEN 10
                        WHEN 'Low' THEN 5
                        ELSE 0
                    END
                )
            FROM assets
            LEFT JOIN vulnerabilities
                ON assets.asset_id = vulnerabilities.asset_id
            GROUP BY
                assets.asset_id,
                assets.asset_name,
                assets.criticality
            ORDER BY assets.asset_id
            """
        )

        assets = cursor.fetchall()

        if not assets:
            print("No assets found. Run the Asset Inventory script first.")
            return

        # Recalculate the current state instead of keeping outdated scores.
        cursor.execute("DELETE FROM risk_scores")

        print("\nNetShield Enterprise Risk Assessment")
        print("-" * 100)

        for asset in assets:
            asset_id = asset[0]
            asset_name = asset[1]
            criticality = asset[2]
            vulnerability_count = asset[3]
            highest_severity_score = asset[4] or 0

            asset_score = ASSET_POINTS.get(criticality, 0)
            vulnerability_count_score = (
                vulnerability_count * VULNERABILITY_COUNT_POINTS
            )

            calculated_score = (
                asset_score
                + highest_severity_score
                + vulnerability_count_score
            )

            # The database only accepts scores between 0 and 100.
            total_score = min(calculated_score, 100)
            risk_level = calculate_risk_level(total_score)
            highest_severity = get_highest_severity(
                highest_severity_score
            )

            calculation_reason = (
                f"Asset criticality: {criticality} "
                f"({asset_score} points); "
                f"highest vulnerability severity: "
                f"{highest_severity} "
                f"({highest_severity_score} points); "
                f"vulnerability count: {vulnerability_count} "
                f"({vulnerability_count_score} points)"
            )

            cursor.execute(
                """
                INSERT INTO risk_scores (
                    asset_id,
                    risk_score,
                    risk_level,
                    calculation_reason
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    asset_id,
                    total_score,
                    risk_level,
                    calculation_reason,
                ),
            )

            print(
                f"{asset_name:<25} | "
                f"Score: {total_score:<3} | "
                f"Risk: {risk_level:<8} | "
                f"Asset: {criticality:<8} | "
                f"Highest vulnerability: {highest_severity}"
            )

        connection.commit()

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Risk scoring failed: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    calculate_risk_scores()
