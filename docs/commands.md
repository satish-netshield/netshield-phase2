# Commands Reference

## Run Project Scripts

Run the database initialization:

```bash
python3 scripts/01_db_init.py
```

Run the Asset Inventory:

```bash
python3 scripts/02_asset_inventory.py
```

Run Vulnerability Tracking:

```bash
python3 scripts/03_vulnerability_tracker.py
```

Run the Risk Scoring Engine:

```bash
python3 scripts/04_risk_scoring.py
```

Run Event Detection:

```bash
python3 scripts/05_event_detector.py
```

Run Severity Classification:

```bash
python3 scripts/06_severity_classifier.py
```

Run Incident Timeline Management:

```bash
python3 scripts/07_incident_timeline.py
```

Run Enterprise Dashboard:

```bash
python3 scripts/08_enterprise_dashboard.py
```

---

## SQLite Commands

Show all tables:

```bash
sqlite3 data/enterprise.db ".tables"
```

View all assets:

```bash
sqlite3 data/enterprise.db "SELECT * FROM assets;"
```

Count stored assets:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM assets;"
```

View all vulnerabilities:

```bash
sqlite3 data/enterprise.db "SELECT * FROM vulnerabilities;"
```

Count stored vulnerabilities:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM vulnerabilities;"
```

Test foreign-key protection:

```bash
sqlite3 data/enterprise.db "PRAGMA foreign_keys = ON; INSERT INTO vulnerabilities (asset_id, vulnerability_name, severity, description) VALUES (999, 'Invalid Test Vulnerability', 'High', 'Foreign key test');"
```

View stored risk scores:

```bash
sqlite3 data/enterprise.db "SELECT asset_id, risk_score, risk_level, calculation_reason FROM risk_scores;"
```

Count detected incidents:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM incidents;"
```

View incident details:

```bash
sqlite3 data/enterprise.db "SELECT incident_id, asset_id, incident_type, source_ip, severity, status, description FROM incidents;"
```

Count incidents by severity:

```bash
sqlite3 data/enterprise.db "SELECT severity, COUNT(*) FROM incidents GROUP BY severity ORDER BY COUNT(*) DESC;"
```

View classified incidents:

```bash
sqlite3 data/enterprise.db "SELECT incident_id, initial_severity, severity, classification_reason FROM incidents;"
```

Count incidents by final severity:

```bash
sqlite3 data/enterprise.db "SELECT severity, COUNT(*) FROM incidents GROUP BY severity ORDER BY severity;"
```

View the incidents table schema:

```bash
sqlite3 data/enterprise.db ".schema incidents"
```

View all timeline events:

```bash
sqlite3 data/enterprise.db "SELECT * FROM incident_timeline;"
```

View timeline events in chronological order:

```bash
sqlite3 data/enterprise.db "SELECT timeline_id, incident_id, event_type, event_description, event_time FROM incident_timeline ORDER BY timeline_id;"
```

View current incident status:

```bash
sqlite3 data/enterprise.db "SELECT incident_id, incident_type, severity, status FROM incidents ORDER BY incident_id;"
```

Count stored timeline events:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM incident_timeline;"
```

Count timeline events for each incident:

```bash
sqlite3 data/enterprise.db "SELECT incident_id, COUNT(*) FROM incident_timeline GROUP BY incident_id ORDER BY incident_id;"
```

View the Incident Timeline table schema:

```bash
sqlite3 data/enterprise.db ".schema incident_timeline"
```

Verify Enterprise Dashboard data:

```bash
sqlite3 data/enterprise.db "
SELECT
(SELECT COUNT(*) FROM assets),
(SELECT COUNT(*) FROM vulnerabilities),
(SELECT COUNT(*) FROM risk_scores),
(SELECT COUNT(*) FROM incidents),
(SELECT COUNT(*) FROM incident_timeline);
"
```

Expected Output:

```text
4|4|4|3|9
```

---

## Git Commands

Check repository status:

```bash
git status
```

Stage all changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "commit message"
```

Push changes to GitHub:

```bash
git push
```

---

## System Validation

Run the complete project from a clean database in the following order:

```text
01_db_init.py
        ↓
02_asset_inventory.py
        ↓
03_vulnerability_tracker.py
        ↓
04_risk_scoring.py
        ↓
05_event_detector.py
        ↓
06_severity_classifier.py
        ↓
07_incident_timeline.py
        ↓
08_enterprise_dashboard.py
        ↓
Verify database totals
```

---

## Development Workflow

```text
Plan
  ↓
Build
  ↓
Run
  ↓
Test
  ↓
Update Documentation
  ↓
Review Documentation
  ↓
Git Commit
  ↓
Git Push
  ↓
Next Component
```
---
