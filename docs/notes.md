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

---

## Enterprise Dashboard

The Enterprise Dashboard provides a read-only summary of the current enterprise security posture. It combines asset, vulnerability, risk, incident, and timeline information into one terminal view.

### Notes from Testing

- The dashboard displayed data from all five main database areas.
- Asset, vulnerability, risk, incident, and timeline totals matched the database.
- Risk levels were displayed as two Critical, one High, one Medium, and zero Low.
- Incident severity totals were displayed as one Critical and two High.
- Incident statuses were displayed as one Investigating, one Contained, and one Resolved.
- Priority incidents were ordered by final severity.
- Recent timeline activity was displayed in reverse chronological order.
- Repeated execution did not create, update, or delete any database records.
- Database counts remained unchanged at `4|4|4|3|9`.

### Engineering Observations

The first dashboard version displayed only the final incident severity. During review, I realised this did not clearly show whether the Severity Classification component had changed the original priority. I updated the Priority Incident Summary to display the transition from initial to final severity.

The first version showed initial severity, final severity, and the change as separate values. I simplified the display to use a single line such as `High -> Critical (Escalated)`. The dashboard became cleaner and easier to understand while still showing the most important information.

### What I Learned

- A dashboard should explain important changes, not only show the latest values.
- Showing initial and final severity makes classification decisions easier to review.
- Clear presentation is just as important as accurate data.
- Small changes to the output can make information easier for an analyst to understand.
- A reporting component should remain read-only and should not modify operational data.

### Next Expansion Scope or Idea

- Add assigned analyst information.
- Show investigation duration and response times.
- Add filtering by severity, status, or asset.
- Display security trends over time.
- Export dashboard results to CSV or another report format.

---

# System Validation

The System Validation component confirms that every NetShield Enterprise component works correctly from a clean installation.

Instead of testing components individually, the project is rebuilt from an empty database and every component is executed in sequence. This verifies that the complete workflow functions correctly and that a new user can run the project successfully from start to finish.

### Notes from Testing

- The existing database was removed before testing began.
- A new database was created successfully.
- All five database tables were created correctly.
- Every project component completed successfully.
- The final database totals were verified as `4|4|4|3|9`.
- Two integration issues were identified during clean-state testing.
- Both issues were corrected and the complete workflow was successfully revalidated.
- The final validation confirmed the complete project works from a clean installation.

### Engineering Observations

- During clean-state testing I found two issues that were not visible during normal development. One was in the database creation script, and the other was in the incident insertion logic.
- These issues only appeared after deleting the database and rebuilding the entire project from the beginning. This confirmed that testing from a fresh installation is just as important as testing individual components.

### What I Learned

- Running every component from a clean database is the best way to confirm the project works from start to finish.
- Database changes should always be checked against every script that reads from or writes to that table.
- Testing each component is important, but end-to-end testing is what confirms the whole system works together.
- Small issues can remain hidden until the complete workflow is tested from the beginning.
- Fixing problems found during validation makes the project more reliable for anyone using it for the first time.

### Next Expansion Scope or Idea

- Test the project using larger enterprise datasets.
- Add automated validation for future project builds.
- Generate validation reports automatically.
- Add regression testing before future releases.
- Validate the project across different operating systems.
