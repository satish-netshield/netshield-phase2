# Project Notes

## Database Initialization

The database initialization script creates the SQLite database and prepares the core tables required for the project.

The script can be executed multiple times safely because each table is created only if it does not already exist.

### Notes from Testing

- Database created successfully.
- All five tables were verified using SQLite.
- Foreign key support was enabled successfully.

---

## Asset Inventory

The Asset Inventory component stores enterprise assets and displays the current inventory.

The script uses parameterised SQL queries to safely insert asset records while preventing duplicate IP addresses.

### Notes from Testing

- Four sample assets were added successfully.
- Asset records were displayed correctly.
- Duplicate IP addresses were rejected.
- Existing records remained unchanged after multiple test runs.

---

## Vulnerability Tracking

The Vulnerability Tracking component records security weaknesses against existing enterprise assets.

The script checks for duplicate records before inserting new vulnerabilities and displays the inventory ordered by severity.

### Notes from Testing

- Four vulnerabilities were stored successfully.
- Vulnerabilities were linked to the correct assets.
- Duplicate vulnerability records were prevented.
- Foreign-key validation successfully rejected invalid asset IDs.

---

## Risk Scoring Engine

The Risk Scoring Engine calculates a current risk score for every asset using asset criticality, highest vulnerability severity, and vulnerability count.

Existing risk records are deleted before recalculation so the table represents the latest assessment rather than storing duplicate historical scores.

### Notes from Testing

- Four asset risk scores were calculated successfully.
- The Database Server received the highest score of 75.
- Calculation reasons were stored with each score.
- Re-running the script kept the risk-score count at four.

