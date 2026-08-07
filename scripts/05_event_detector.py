from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"

FAILED_LOGIN_THRESHOLD = 3


def connect_database() -> sqlite3.Connection:
    """Connect to the enterprise database with foreign keys enabled."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_asset_details(
    connection: sqlite3.Connection,
    asset_id: int,
) -> tuple[str, str] | None:
    """Return the asset name and criticality for an asset ID."""

    return connection.execute(
        """
        SELECT asset_name, criticality
        FROM assets
        WHERE asset_id = ?
        """,
        (asset_id,),
    ).fetchone()


def detect_event(
    event: dict,
    asset_name: str,
    asset_criticality: str,
) -> tuple[str, str, str] | None:
    """Apply detection rules and return incident details when suspicious."""

    event_type = event["event_type"]
    username = event["username"]
    location = event["location"]
    network_type = event["network_type"]
    source_ip = event["source_ip"]
    failed_attempts = event.get("failed_attempts", 0)
    outside_business_hours = event.get(
        "outside_business_hours",
        False,
    )

    if (
        event_type == "Failed Login"
        and failed_attempts >= FAILED_LOGIN_THRESHOLD
    ):
        incident_type = "Possible Brute Force Attempt"
        severity = "High"

        description = (
            f"{failed_attempts} failed login attempts detected for user "
            f"{username} on {asset_name}. Source IP: {source_ip}; "
            f"location: {location}; network: {network_type}."
        )

        return incident_type, severity, description

    if (
        event_type == "USB Inserted"
        and network_type == "Public Wi-Fi"
        and location == "Unknown"
    ):
        incident_type = "Suspicious USB Activity"
        severity = "Medium"

        description = (
            f"USB activity detected for user {username} on {asset_name} "
            f"while connected through Public Wi-Fi from an unknown "
            f"location. Source IP: {source_ip}."
        )

        return incident_type, severity, description

    if (
        event_type == "Successful Login"
        and outside_business_hours
        and asset_criticality == "Critical"
    ):
        incident_type = "After-Hours Critical Asset Access"
        severity = "High"

        description = (
            f"User {username} accessed critical asset {asset_name} "
            f"outside business hours. Source IP: {source_ip}; "
            f"location: {location}; network: {network_type}."
        )

        return incident_type, severity, description

    return None


def incident_exists(
    connection: sqlite3.Connection,
    asset_id: int,
    incident_type: str,
    source_ip: str,
    description: str,
) -> bool:
    """Check whether the detected incident has already been stored."""

    result = connection.execute(
        """
        SELECT 1
        FROM incidents
        WHERE asset_id = ?
          AND incident_type = ?
          AND COALESCE(source_ip, '') = COALESCE(?, '')
          AND description = ?
        LIMIT 1
        """,
        (
            asset_id,
            incident_type,
            source_ip,
            description,
        ),
    ).fetchone()

    return result is not None


def store_incident(
    connection: sqlite3.Connection,
    asset_id: int,
    incident_type: str,
    source_ip: str,
    description: str,
    severity: str,
) -> bool:
    """Store a newly detected incident."""

    if incident_exists(
        connection,
        asset_id,
        incident_type,
        source_ip,
        description,
    ):
        print(f"Existing detection skipped: {incident_type}")
        return False

    connection.execute(
        """
        INSERT INTO incidents (
            asset_id,
            incident_type,
            source_ip,
            description,
            initial_severity,
            severity,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, 'Open')
        """,
        (
            asset_id,
            incident_type,
            source_ip,
            description,
            severity,
            severity,
        ),
    )

    print(f"Suspicious event detected: {incident_type}")
    return True


def process_events(events: list[dict]) -> None:
    """Analyse simulated events and store suspicious detections."""

    connection = connect_database()
    detected_count = 0
    normal_count = 0

    try:
        print("\nNetShield Enterprise Event Detection")
        print("-" * 100)

        for event in events:
            asset_details = get_asset_details(
                connection,
                event["asset_id"],
            )

            if asset_details is None:
                print(
                    "Event skipped because asset does not exist: "
                    f"{event['asset_id']}"
                )
                continue

            asset_name, asset_criticality = asset_details

            detection = detect_event(
                event,
                asset_name,
                asset_criticality,
            )

            if detection is None:
                normal_count += 1
                print(
                    f"Normal activity: {event['event_type']} "
                    f"on {asset_name}"
                )
                continue

            incident_type, severity, description = detection

            stored = store_incident(
                connection,
                event["asset_id"],
                incident_type,
                event["source_ip"],
                description,
                severity,
            )

            if stored:
                detected_count += 1

        connection.commit()

        print("-" * 100)
        print(f"New suspicious events stored: {detected_count}")
        print(f"Normal events reviewed: {normal_count}")

    except sqlite3.Error as error:
        connection.rollback()
        print(f"Event detection failed: {error}")
        raise

    finally:
        connection.close()


def list_detected_incidents() -> None:
    """Display all detected incidents with their related assets."""

    connection = connect_database()

    try:
        incidents = connection.execute(
            """
            SELECT
                incidents.incident_id,
                assets.asset_name,
                incidents.incident_type,
                incidents.source_ip,
                incidents.severity,
                incidents.status,
                incidents.detected_at
            FROM incidents
            JOIN assets
                ON incidents.asset_id = assets.asset_id
            ORDER BY incidents.incident_id
            """
        ).fetchall()

        if not incidents:
            print("\nNo suspicious events have been detected.")
            return

        print("\nDetected Security Incidents")
        print("-" * 115)

        for incident in incidents:
            print(
                f"ID: {incident[0]} | "
                f"Asset: {incident[1]} | "
                f"Type: {incident[2]} | "
                f"Source IP: {incident[3]} | "
                f"Severity: {incident[4]} | "
                f"Status: {incident[5]} | "
                f"Detected: {incident[6]}"
            )

    finally:
        connection.close()


def get_sample_events() -> list[dict]:
    """Return simulated enterprise events for detector testing."""

    return [
        {
            "asset_id": 1,
            "event_type": "Failed Login",
            "username": "priya.sharma",
            "source_ip": "203.0.113.25",
            "location": "Auckland",
            "network_type": "Home",
            "failed_attempts": 5,
            "outside_business_hours": False,
        },
        {
            "asset_id": 2,
            "event_type": "Successful Login",
            "username": "daniel.lee",
            "source_ip": "10.0.20.15",
            "location": "Auckland Office",
            "network_type": "Corporate",
            "failed_attempts": 0,
            "outside_business_hours": False,
        },
        {
            "asset_id": 3,
            "event_type": "Successful Login",
            "username": "database.admin",
            "source_ip": "198.51.100.42",
            "location": "Unknown",
            "network_type": "VPN",
            "failed_attempts": 0,
            "outside_business_hours": True,
        },
        {
            "asset_id": 4,
            "event_type": "USB Inserted",
            "username": "network.admin",
            "source_ip": "192.0.2.18",
            "location": "Unknown",
            "network_type": "Public Wi-Fi",
            "failed_attempts": 0,
            "outside_business_hours": False,
        },
    ]


if __name__ == "__main__":
    sample_events = get_sample_events()
    process_events(sample_events)
    list_detected_incidents()
