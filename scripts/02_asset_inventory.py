from pathlib import Path
import sqlite3


BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = BASE_DIR / "data" / "enterprise.db"


def connect_database() -> sqlite3.Connection:
    """Connect to the enterprise database with foreign keys enabled."""

    connection = sqlite3.connect(DATABASE_PATH)
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def add_asset(
    asset_name: str,
    asset_type: str,
    department: str,
    owner: str,
    operating_system: str,
    ip_address: str,
    criticality: str,
) -> None:
    """Add an enterprise asset to the inventory."""

    connection = connect_database()

    try:
        connection.execute(
            """
            INSERT INTO assets (
                asset_name,
                asset_type,
                department,
                owner,
                operating_system,
                ip_address,
                criticality
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                asset_name,
                asset_type,
                department,
                owner,
                operating_system,
                ip_address,
                criticality,
            ),
        )

        connection.commit()
        print(f"Asset added successfully: {asset_name}")

    except sqlite3.IntegrityError:
        connection.rollback()
        print(f"Asset already exists or uses a duplicate IP: {asset_name}")

    finally:
        connection.close()


def list_assets() -> None:
    """Display all assets currently stored in the inventory."""

    connection = connect_database()

    try:
        assets = connection.execute(
            """
            SELECT
                asset_id,
                asset_name,
                asset_type,
                department,
                owner,
                operating_system,
                ip_address,
                criticality,
                status
            FROM assets
            ORDER BY asset_id
            """
        ).fetchall()

        if not assets:
            print("No assets found.")
            return

        print("\nNetShield Enterprise Asset Inventory")
        print("-" * 90)

        for asset in assets:
            print(
                f"ID: {asset[0]} | "
                f"Name: {asset[1]} | "
                f"Type: {asset[2]} | "
                f"Department: {asset[3]} | "
                f"Owner: {asset[4]} | "
                f"OS: {asset[5]} | "
                f"IP: {asset[6]} | "
                f"Criticality: {asset[7]} | "
                f"Status: {asset[8]}"
            )

    finally:
        connection.close()


def seed_sample_assets() -> None:
    """Insert sample enterprise assets for testing."""

    sample_assets = [
        (
            "Finance-Laptop-01",
            "Laptop",
            "Finance",
            "Priya Sharma",
            "Windows 11",
            "10.0.10.21",
            "High",
        ),
        (
            "HR-Laptop-01",
            "Laptop",
            "Human Resources",
            "Daniel Lee",
            "Windows 11",
            "10.0.20.15",
            "Medium",
        ),
        (
            "Database-Server-01",
            "Server",
            "IT",
            "Infrastructure Team",
            "Ubuntu Server",
            "10.0.30.10",
            "Critical",
        ),
        (
            "VPN-Gateway-01",
            "Network Device",
            "IT",
            "Network Team",
            "Linux Appliance",
            "10.0.40.5",
            "Critical",
        ),
    ]

    for asset in sample_assets:
        add_asset(*asset)


if __name__ == "__main__":
    seed_sample_assets()
    list_assets()
