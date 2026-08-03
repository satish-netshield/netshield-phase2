#!/usr/bin/env python3
"""Display a read-only summary of the NetShield enterprise security posture."""

import sqlite3
from pathlib import Path

DATABASE_PATH = Path(__file__).resolve().parent.parent / "data" / "enterprise.db"
LINE_WIDTH = 111

RISK_LEVELS = ("Critical", "High", "Medium", "Low")
SEVERITY_LEVELS = ("Critical", "High", "Medium", "Low")
INCIDENT_STATUSES = ("Open", "Investigating", "Contained", "Resolved")


def print_section(title: str) -> None:
    """Print a consistent dashboard section heading."""
    print()
    print(title)
    print("-" * LINE_WIDTH)


def get_table_count(
    connection: sqlite3.Connection,
    table_name: str,
) -> int:
    """Return the total number of records in an approved table."""
    allowed_tables = {
        "assets",
        "vulnerabilities",
        "risk_scores",
        "incidents",
        "incident_timeline",
    }

    if table_name not in allowed_tables:
        raise ValueError(f"Unsupported table requested: {table_name}")

    cursor = connection.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()

    return int(result[0]) if result else 0


def get_grouped_counts(
    connection: sqlite3.Connection,
    table_name: str,
    column_name: str,
    expected_values: tuple[str, ...],
) -> dict[str, int]:
    """Return grouped counts while keeping missing categories visible as zero."""
    allowed_pairs = {
        ("risk_scores", "risk_level"),
        ("incidents", "severity"),
        ("incidents", "status"),
    }

    if (table_name, column_name) not in allowed_pairs:
        raise ValueError(
            f"Unsupported grouped query: {table_name}.{column_name}"
        )

    counts = {value: 0 for value in expected_values}

    cursor = connection.execute(
        f"""
        SELECT {column_name}, COUNT(*)
        FROM {table_name}
        GROUP BY {column_name}
        """
    )

    for value, count in cursor.fetchall():
        if value in counts:
            counts[value] = int(count)

    return counts


def display_enterprise_summary(connection: sqlite3.Connection) -> None:
    """Display record totals from the main enterprise tables."""
    print_section("Enterprise Overview")

    summary_items = (
        ("Total Assets", get_table_count(connection, "assets")),
        (
            "Total Vulnerabilities",
            get_table_count(connection, "vulnerabilities"),
        ),
        (
            "Total Risk Assessments",
            get_table_count(connection, "risk_scores"),
        ),
        ("Total Incidents", get_table_count(connection, "incidents")),
        (
            "Timeline Events",
            get_table_count(connection, "incident_timeline"),
        ),
    )

    for label, count in summary_items:
        print(f"{label:<35}: {count}")


def display_risk_summary(connection: sqlite3.Connection) -> None:
    """Display the number of assets at each current risk level."""
    print_section("Asset Risk Summary")

    counts = get_grouped_counts(
        connection,
        "risk_scores",
        "risk_level",
        RISK_LEVELS,
    )

    for risk_level in RISK_LEVELS:
        print(f"{risk_level + ' Risk Assets':<35}: {counts[risk_level]}")


def display_incident_severity(connection: sqlite3.Connection) -> None:
    """Display incidents grouped by final severity."""
    print_section("Incident Severity Summary")

    counts = get_grouped_counts(
        connection,
        "incidents",
        "severity",
        SEVERITY_LEVELS,
    )

    for severity in SEVERITY_LEVELS:
        print(f"{severity + ' Severity':<35}: {counts[severity]}")


def display_incident_status(connection: sqlite3.Connection) -> None:
    """Display incidents grouped by current investigation status."""
    print_section("Incident Status Summary")

    counts = get_grouped_counts(
        connection,
        "incidents",
        "status",
        INCIDENT_STATUSES,
    )

    for status in INCIDENT_STATUSES:
        print(f"{status:<35}: {counts[status]}")


def display_priority_incidents(connection: sqlite3.Connection) -> None:
    """Display priority incidents and show severity changes clearly."""
    print_section("Priority Incident Summary")

    cursor = connection.execute(
        """
        SELECT
            incidents.incident_id,
            assets.asset_name,
            incidents.incident_type,
            incidents.initial_severity,
            incidents.severity,
            incidents.status
        FROM incidents
        INNER JOIN assets
            ON incidents.asset_id = assets.asset_id
        ORDER BY
            CASE incidents.severity
                WHEN 'Critical' THEN 1
                WHEN 'High' THEN 2
                WHEN 'Medium' THEN 3
                WHEN 'Low' THEN 4
                ELSE 5
            END,
            incidents.incident_id
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    if not rows:
        print("No incidents are currently stored.")
        return

    severity_values = {
        "Low": 1,
        "Medium": 2,
        "High": 3,
        "Critical": 4,
    }

    for (
        incident_id,
        asset_name,
        incident_type,
        initial_severity,
        final_severity,
        status,
    ) in rows:
        initial_value = severity_values.get(initial_severity, 0)
        final_value = severity_values.get(final_severity, 0)

        if final_value > initial_value:
            severity_change = "Escalated"
        elif final_value < initial_value:
            severity_change = "Reduced"
        else:
            severity_change = "Unchanged"

        print()
        print(f"ID: {incident_id} | Asset: {asset_name}")
        print(f"Type: {incident_type}")
        print(
            f"Severity: {initial_severity} -> {final_severity} "
            f"({severity_change})"
        )
        print(f"Status: {status}")


def display_recent_activity(connection: sqlite3.Connection) -> None:
    """Display the latest investigation events in reverse chronological order."""
    print_section("Recent Timeline Activity")

    cursor = connection.execute(
        """
        SELECT
            incident_timeline.incident_id,
            assets.asset_name,
            incident_timeline.event_type,
            incident_timeline.event_description,
            incident_timeline.event_time
        FROM incident_timeline
        INNER JOIN incidents
            ON incident_timeline.incident_id = incidents.incident_id
        INNER JOIN assets
            ON incidents.asset_id = assets.asset_id
        ORDER BY incident_timeline.timeline_id DESC
        LIMIT 5
        """
    )

    rows = cursor.fetchall()

    if not rows:
        print("No timeline activity is currently stored.")
        return

    for incident_id, asset_name, event_type, description, event_time in rows:
        print(
            f"[{event_time}] Incident {incident_id} | "
            f"Asset: {asset_name} | {event_type}"
        )
        print(f"  {description}")


def display_dashboard(connection: sqlite3.Connection) -> None:
    """Display all dashboard sections using current database information."""
    print()
    print("=" * LINE_WIDTH)
    print("NETSHIELD ENTERPRISE DASHBOARD".center(LINE_WIDTH))
    print("=" * LINE_WIDTH)

    display_enterprise_summary(connection)
    display_risk_summary(connection)
    display_incident_severity(connection)
    display_incident_status(connection)
    display_priority_incidents(connection)
    display_recent_activity(connection)

    print()
    print("=" * LINE_WIDTH)
    print("Dashboard generated from the current enterprise database.".center(
        LINE_WIDTH
    ))
    print("=" * LINE_WIDTH)


def main() -> None:
    """Connect to the database and display the enterprise dashboard."""
    if not DATABASE_PATH.exists():
        raise FileNotFoundError(
            f"Enterprise database not found: {DATABASE_PATH}"
        )

    connection = sqlite3.connect(DATABASE_PATH)

    try:
        connection.execute("PRAGMA foreign_keys = ON")
        display_dashboard(connection)

    except sqlite3.Error as error:
        print(f"Dashboard generation failed: {error}")
        raise

    finally:
        connection.close()


if __name__ == "__main__":
    main()
