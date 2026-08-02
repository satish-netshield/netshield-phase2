from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"

STATUS_ORDER = {
    "Open": 0,
    "Investigating": 1,
    "Contained": 2,
    "Resolved": 3,
}

INCIDENT_RESPONSE_PLANS = {
    "Possible Brute Force Attempt": {
        "target_status": "Investigating",
        "steps": [
            (
                "Investigating",
                "SOC analyst began reviewing failed login activity, "
                "the affected account, and the source IP address.",
            ),
        ],
    },
    "After-Hours Critical Asset Access": {
        "target_status": "Contained",
        "steps": [
            (
                "Investigating",
                "SOC analyst began reviewing the privileged account, "
                "VPN activity, and access time.",
            ),
            (
                "Contained",
                "The privileged session was terminated and the account "
                "was temporarily restricted pending further review.",
            ),
        ],
    },
    "Suspicious USB Activity": {
        "target_status": "Resolved",
        "steps": [
            (
                "Investigating",
                "SOC analyst reviewed the user, device activity, "
                "network connection, and unknown location.",
            ),
            (
                "Contained",
                "USB access was disabled temporarily while the device "
                "and user activity were validated.",
            ),
            (
                "Resolved",
                "The activity was confirmed as authorised maintenance. "
                "The incident was documented and closed.",
            ),
        ],
    },
}


def connect_database() -> sqlite3.Connection:
    """Connect to the enterprise database with foreign keys enabled."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def timeline_event_exists(
    connection: sqlite3.Connection,
    incident_id: int,
    event_type: str,
    event_description: str,
) -> bool:
    """Check whether the same timeline event is already stored."""

    result = connection.execute(
        """
        SELECT 1
        FROM incident_timeline
        WHERE incident_id = ?
          AND event_type = ?
          AND event_description = ?
        LIMIT 1
        """,
        (
            incident_id,
            event_type,
            event_description,
        ),
    ).fetchone()

    return result is not None


def add_timeline_event(
    connection: sqlite3.Connection,
    incident_id: int,
    event_type: str,
    event_description: str,
) -> bool:
    """Store a timeline event unless it already exists."""

    if timeline_event_exists(
        connection,
        incident_id,
        event_type,
        event_description,
    ):
        return False

    connection.execute(
        """
        INSERT INTO incident_timeline (
            incident_id,
            event_type,
            event_description
        )
        VALUES (?, ?, ?)
        """,
        (
            incident_id,
            event_type,
            event_description,
        ),
    )

    return True


def record_initial_detection(
    connection: sqlite3.Connection,
    incident_id: int,
    incident_type: str,
    initial_severity: str,
) -> bool:
    """Backfill the original incident detection into the timeline."""

    description = (
        f"Incident detected as {incident_type} with an initial severity "
        f"of {initial_severity} and status Open."
    )

    return add_timeline_event(
        connection,
        incident_id,
        "Incident Detected",
        description,
    )


def apply_status_change(
    connection: sqlite3.Connection,
    incident_id: int,
    current_status: str,
    new_status: str,
    analyst_note: str,
) -> bool:
    """Apply a valid forward status transition and record it."""

    expected_next_position = STATUS_ORDER[current_status] + 1

    if STATUS_ORDER[new_status] != expected_next_position:
        raise ValueError(
            f"Invalid status transition: {current_status} -> {new_status}"
        )

    description = (
        f"Status changed from {current_status} to {new_status}. "
        f"Analyst note: {analyst_note}"
    )

    event_added = add_timeline_event(
        connection,
        incident_id,
        "Status Change",
        description,
    )

    connection.execute(
        """
        UPDATE incidents
        SET status = ?
        WHERE incident_id = ?
        """,
        (
            new_status,
            incident_id,
        ),
    )

    return event_added


def manage_incident_timelines() -> None:
    """Record and update the investigation lifecycle of each incident."""

    connection = connect_database()

    try:
        incidents = connection.execute(
            """
            SELECT
                incident_id,
                incident_type,
                initial_severity,
                severity,
                status
            FROM incidents
            ORDER BY incident_id
            """
        ).fetchall()

        if not incidents:
            print("No incidents found for timeline management.")
            return

        new_timeline_events = 0
        status_updates = 0

        print("\nNetShield Enterprise Incident Timeline Management")
        print("-" * 115)

        for incident in incidents:
            incident_id = incident[0]
            incident_type = incident[1]
            initial_severity = incident[2]
            final_severity = incident[3]
            current_status = incident[4]

            print(
                f"ID: {incident_id} | "
                f"Incident: {incident_type} | "
                f"Severity: {final_severity} | "
                f"Starting Status: {current_status}"
            )

            if record_initial_detection(
                connection,
                incident_id,
                incident_type,
                initial_severity,
            ):
                new_timeline_events += 1
                print("  Timeline added: Incident Detected")
            else:
                print("  Existing timeline event skipped: Incident Detected")

            response_plan = INCIDENT_RESPONSE_PLANS.get(incident_type)

            if response_plan is None:
                print("  No response plan configured. Status unchanged.")
                continue

            target_status = response_plan["target_status"]

            if STATUS_ORDER[current_status] > STATUS_ORDER[target_status]:
                print(
                    f"  Current status {current_status} is already beyond "
                    f"the configured target {target_status}."
                )
                continue

            for new_status, analyst_note in response_plan["steps"]:
                if STATUS_ORDER[new_status] <= STATUS_ORDER[current_status]:
                    continue

                event_added = apply_status_change(
                    connection,
                    incident_id,
                    current_status,
                    new_status,
                    analyst_note,
                )

                if event_added:
                    new_timeline_events += 1
                    print(
                        f"  Status updated: "
                        f"{current_status} -> {new_status}"
                    )
                else:
                    print(
                        f"  Existing transition skipped: "
                        f"{current_status} -> {new_status}"
                    )

                status_updates += 1
                current_status = new_status

                if current_status == target_status:
                    break

            print(f"  Final Status: {current_status}")

        connection.commit()

        print("-" * 115)
        print(f"New timeline events stored: {new_timeline_events}")
        print(f"Incident status updates applied: {status_updates}")

    except (sqlite3.Error, ValueError) as error:
        connection.rollback()
        print(f"Incident timeline management failed: {error}")
        raise

    finally:
        connection.close()


def display_incident_timelines() -> None:
    """Display all incidents and their recorded timeline events."""

    connection = connect_database()

    try:
        incidents = connection.execute(
            """
            SELECT
                incidents.incident_id,
                incidents.incident_type,
                incidents.severity,
                incidents.status,
                assets.asset_name
            FROM incidents
            JOIN assets
                ON incidents.asset_id = assets.asset_id
            ORDER BY incidents.incident_id
            """
        ).fetchall()

        print("\nIncident Timeline Results")
        print("=" * 115)

        for incident in incidents:
            incident_id = incident[0]
            incident_type = incident[1]
            severity = incident[2]
            status = incident[3]
            asset_name = incident[4]

            print(
                f"\nIncident ID: {incident_id} | "
                f"Asset: {asset_name} | "
                f"Type: {incident_type} | "
                f"Severity: {severity} | "
                f"Status: {status}"
            )

            timeline_events = connection.execute(
                """
                SELECT
                    event_type,
                    event_description,
                    event_time
                FROM incident_timeline
                WHERE incident_id = ?
                ORDER BY timeline_id
                """,
                (incident_id,),
            ).fetchall()

            if not timeline_events:
                print("  No timeline events recorded.")
                continue

            for event_type, description, event_time in timeline_events:
                print(
                    f"  [{event_time}] {event_type}: "
                    f"{description}"
                )

    finally:
        connection.close()


if __name__ == "__main__":
    manage_incident_timelines()
    display_incident_timelines()
