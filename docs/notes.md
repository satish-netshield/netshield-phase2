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

---

## Event Detection

The Event Detection component analyses simulated activity and stores events that match defined security rules.

The detector confirms that the related asset exists, evaluates event context, prevents duplicate incident records, and stores suspicious activity with an initial severity and Open status.

### Notes from Testing

- Four simulated events were processed.
- Three events matched detection rules.
- One normal login was reviewed without being stored as an incident.
- Duplicate detections were skipped during repeated test runs.
- The final incident count remained at three.
- Severity totals were verified as two High and one Medium.

---

## Severity Classification

The Severity Classification component combines the original detection severity with the affected asset's current risk level.

The original severity is stored separately from the final severity, preventing repeated classification from continuously increasing incident priority.

### Notes from Testing

- Three incidents were classified successfully.
- The brute-force incident remained High.
- The after-hours critical asset incident increased to Critical.
- Suspicious USB activity increased from Medium to High.
- Classification reasons were stored in the incidents table.
- Repeated classification produced stable results.
- The database initialization and Event Detection scripts were updated for fresh project installations.

---

## Incident Timeline Management

The Incident Timeline Management component records the full investigation history of each security incident.

Incidents follow a controlled lifecycle:

```text
Open
  ↓
Investigating
  ↓
Contained
  ↓
Resolved
```

Each status change is stored with an analyst note and timestamp, creating a permanent audit trail. Duplicate timeline events are prevented so repeated executions do not alter or inflate the investigation history.

### Notes from Testing

- Three incidents were processed successfully.
- Nine timeline events were stored.
- Incident 1 progressed from Open to Investigating.
- Incident 2 progressed from Open to Investigating and then Contained.
- Incident 3 progressed through the complete lifecycle to Resolved.
- Analyst notes were stored for every status change.
- Timeline events were displayed in chronological order.
- Re-running the script created no duplicate timeline events.
- Re-running the script applied no additional status updates.
- Timeline totals were verified as two, three, and four events for the three incidents.
