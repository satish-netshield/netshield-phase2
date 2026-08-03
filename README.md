## Asset Inventory

The Asset Inventory component records and manages enterprise assets such as laptops, servers, and network devices.

Each asset includes:

* Asset name
* Asset type
* Department
* Owner
* Operating system
* IP address
* Criticality
* Operational status

Duplicate IP addresses are blocked to prevent conflicting asset records.

### Example Output

```text
NetShield Enterprise Asset Inventory
------------------------------------------------------------------------------------------
ID: 1 | Name: Finance-Laptop-01 | Type: Laptop | Department: Finance | Owner: Priya Sharma | OS: Windows 11 | IP: 10.0.10.21 | Criticality: High | Status: Active
ID: 2 | Name: HR-Laptop-01 | Type: Laptop | Department: Human Resources | Owner: Daniel Lee | OS: Windows 11 | IP: 10.0.20.15 | Criticality: Medium | Status: Active
ID: 3 | Name: Database-Server-01 | Type: Server | Department: IT | Owner: Infrastructure Team | OS: Ubuntu Server | IP: 10.0.30.10 | Criticality: Critical | Status: Active
ID: 4 | Name: VPN-Gateway-01 | Type: Network Device | Department: IT | Owner: Network Team | OS: Linux Appliance | IP: 10.0.40.5 | Criticality: Critical | Status: Active
```

---

## Vulnerability Tracking

The Vulnerability Tracking component records security weaknesses affecting known enterprise assets.

Each vulnerability includes:

* Related asset
* Vulnerability name
* CVE identifier (when available)
* Severity
* Description
* Status
* Discovery timestamp

Vulnerabilities are displayed from highest to lowest severity so the most critical findings are reviewed first.

### Example Output

```text
NetShield Enterprise Vulnerability Inventory
--------------------------------------------------------------------------------------------------------------
ID: 3 | Asset: Database-Server-01 | Vulnerability: Remote Code Execution Exposure | CVE: CVE-2024-6387 | Severity: Critical | Status: Open
ID: 1 | Asset: Finance-Laptop-01 | Vulnerability: Missing Windows Security Updates | CVE: Not assigned | Severity: High | Status: Open
ID: 4 | Asset: VPN-Gateway-01 | Vulnerability: Weak Administrative Password Policy | CVE: Not assigned | Severity: High | Status: Open
ID: 2 | Asset: HR-Laptop-01 | Vulnerability: Outdated Web Browser | CVE: Not assigned | Severity: Medium | Status: Open
```

### Testing Notes

* Four vulnerabilities were linked successfully to existing assets.
* Results were ordered by severity.
* Duplicate vulnerability records were prevented.
* Foreign-key validation prevented vulnerabilities from being linked to non-existent assets.

---

## Risk Scoring Engine

The Risk Scoring Engine calculates an overall risk score for each enterprise asset.

The score combines:

* Asset criticality
* Highest vulnerability severity
* Number of vulnerabilities

### Scoring Model

| Factor                          | Value |
| ------------------------------- | ----: |
| Low asset criticality           |    10 |
| Medium asset criticality        |    20 |
| High asset criticality          |    30 |
| Critical asset criticality      |    40 |
| Low vulnerability severity      |     5 |
| Medium vulnerability severity   |    10 |
| High vulnerability severity     |    20 |
| Critical vulnerability severity |    30 |
| Each vulnerability              |     5 |

The final score is classified as:

| Score  | Risk Level |
| ------ | ---------- |
| 0–20   | Low        |
| 21–40  | Medium     |
| 41–60  | High       |
| 61–100 | Critical   |

### Example Output

```text
NetShield Enterprise Risk Assessment
----------------------------------------------------------------------------------------------------
Finance-Laptop-01         | Score: 55 | Risk: High     | Asset: High     | Highest vulnerability: High
HR-Laptop-01              | Score: 35 | Risk: Medium   | Asset: Medium   | Highest vulnerability: Medium
Database-Server-01        | Score: 75 | Risk: Critical | Asset: Critical | Highest vulnerability: Critical
VPN-Gateway-01            | Score: 65 | Risk: Critical | Asset: Critical | Highest vulnerability: High
```

---

## Event Detection

The Event Detection component analyses simulated enterprise activity and identifies events that may require security investigation.

Current detection rules include:

* Three or more failed login attempts
* After-hours access to a Critical asset
* USB activity from an unknown location while using Public Wi-Fi

Normal activity is reviewed but is not stored as an incident. Suspicious detections are linked to known assets and recorded with an **initial severity** and an `Open` status.

### Example Output

```text
NetShield Enterprise Event Detection
----------------------------------------------------------------------------------------------------
Suspicious event detected: Possible Brute Force Attempt
Normal activity: Successful Login on HR-Laptop-01
Suspicious event detected: After-Hours Critical Asset Access
Suspicious event detected: Suspicious USB Activity
----------------------------------------------------------------------------------------------------
New suspicious events stored: 3
Normal events reviewed: 1
```

### Detected Incidents

```text
ID: 1 | Asset: Finance-Laptop-01 | Type: Possible Brute Force Attempt | Initial Severity: High | Status: Open
ID: 2 | Asset: Database-Server-01 | Type: After-Hours Critical Asset Access | Initial Severity: High | Status: Open
ID: 3 | Asset: VPN-Gateway-01 | Type: Suspicious USB Activity | Initial Severity: Medium | Status: Open
```

### Testing Notes

* Four simulated events were analysed.
* Three suspicious events were stored as incidents.
* One normal login was reviewed without creating an incident.
* Re-running the detector did not create duplicate incidents.
* The initial detections included two High-severity and one Medium-severity incident.

---

## Severity Classification

The Severity Classification component reviews each detected incident using its initial severity and the current risk level of the affected asset.

The classifier uses a simple point-based scoring model.

### Initial Severity Points

| Initial Severity | Points |
| ---------------- | -----: |
| Low              |     10 |
| Medium           |     20 |
| High             |     30 |
| Critical         |     40 |

### Asset Risk Points

| Asset Risk | Points |
| ---------- | -----: |
| Low        |     10 |
| Medium     |     20 |
| High       |     30 |
| Critical   |     40 |

The combined score determines the final incident severity.

### Classification Thresholds

| Classification Score | Final Severity |
| -------------------- | -------------- |
| 0–20                 | Low            |
| 21–40                | Medium         |
| 41–60                | High           |
| 61–80                | Critical       |

The original detection severity is preserved separately so repeated classification always begins from the same starting point.

### Example Output

```text
NetShield Enterprise Severity Classification
-------------------------------------------------------------------------------------------------------------------
ID: 1 | Asset: Finance-Laptop-01 | Initial: High | Asset Risk: High | Score: 60 | Final: High
ID: 2 | Asset: Database-Server-01 | Initial: High | Asset Risk: Critical | Score: 70 | Final: Critical
ID: 3 | Asset: VPN-Gateway-01 | Initial: Medium | Asset Risk: Critical | Score: 60 | Final: High
```

### Testing Notes

* Three incidents were classified successfully.
* One incident remained High.
* One incident increased from High to Critical.
* One incident increased from Medium to High.
* Classification reasons were stored for every incident.
* Re-running the classifier did not cause repeated escalation.

---

## Incident Timeline Management

Once an incident has been detected and classified, it moves into the investigation stage. This component records every step of the investigation, updates the incident status, stores analyst notes, and builds a complete timeline from detection through to resolution.

A structured workflow makes it easy to understand what has happened, what actions have already been taken, and the current state of the investigation. It also keeps the incident history accurate when the component is executed multiple times.

### Investigation Workflow

```text
Open
  ↓
Investigating
  ↓
Contained
  ↓
Resolved
```

### Key Capabilities

- Records each stage of the incident investigation lifecycle.
- Updates the current incident status as the investigation progresses.
- Stores analyst notes alongside every status change.
- Builds a chronological timeline for each incident.
- Prevents duplicate timeline events during repeated execution.
- Preserves a complete investigation history for reporting and future review.

### Example Output

```text
Incident ID: 2
Type: After-Hours Critical Asset Access
Severity: Critical
Current Status: Contained

Timeline
--------------------------------------------------
[23:33:31] Incident Detected

↓

[23:33:31] Status changed from Open to Investigating
SOC analyst reviewed the privileged account,
VPN activity, and access time.

↓

[23:33:31] Status changed from Investigating to Contained
The privileged session was terminated and the
account was temporarily restricted pending review.
```

### Testing Notes

- Three incidents were processed successfully.
- Nine timeline events were created across all incidents.
- Incident statuses progressed correctly through the investigation lifecycle.
- Analyst notes were recorded for every status update.
- Timeline events were displayed in chronological order.
- Re-running the component did not create duplicate timeline events.
- Re-running the component did not apply additional status updates.
- Investigation history remained unchanged during repeated testing.

---

## Enterprise Dashboard

The Enterprise Dashboard brings together information from every previous component into a single read-only view. It provides a summary of enterprise assets, vulnerabilities, risk assessments, incidents, and investigation activity, helping analysts quickly understand the current security posture.

The dashboard only reads information from the database. It does not create, update, or delete any records, making it safe to use for reporting and daily operational monitoring.

### Workflow

```text
Enterprise Database
        │
        ├── Assets
        ├── Vulnerabilities
        ├── Risk Scores
        ├── Incidents
        └── Incident Timeline
                 │
                 ▼
        Enterprise Dashboard
                 │
                 ▼
     Consolidated Security Summary
```

### Key Capabilities

- Displays a consolidated view of enterprise security information.
- Summarises enterprise assets, vulnerabilities, risk assessments, incidents, and timeline events.
- Groups assets by current risk level.
- Groups incidents by current severity and investigation status.
- Shows priority incidents using the latest classified severity.
- Displays the severity transition from initial to final classification.
- Displays the most recent investigation activity.
- Operates in read-only mode without modifying enterprise data.

### Example Output

```text
Enterprise Overview
------------------------------------------------------------
Total Assets               : 4
Total Vulnerabilities      : 4
Total Risk Assessments     : 4
Total Incidents            : 3
Timeline Events            : 9

Priority Incident Summary

ID: 2 | Asset: Database-Server-01
Type: After-Hours Critical Asset Access
Severity: High -> Critical (Escalated)
Status: Contained

ID: 1 | Asset: Finance-Laptop-01
Type: Possible Brute Force Attempt
Severity: High -> High (Unchanged)
Status: Investigating

ID: 3 | Asset: VPN-Gateway-01
Type: Suspicious USB Activity
Severity: Medium -> High (Escalated)
Status: Resolved
```

### Testing Notes

- The dashboard displayed information from all enterprise components.
- Asset, vulnerability, risk, incident, and timeline totals matched the database.
- Priority incidents were displayed using the final classified severity.
- Severity transitions were displayed correctly for every incident.
- Recent investigation activity was displayed in reverse chronological order.
- Re-running the dashboard did not create, modify, or delete database records.
- Database verification confirmed the dashboard operates in read-only mode.

### Engineering Observations

- During testing I realised that displaying only the final severity did not clearly show how the classification process changed an incident's priority. I updated the dashboard to display the transition from the initial severity to the final severity.
- I first displayed the initial severity, final severity, and change as separate values. Replacing them with a single format such as `High -> Critical (Escalated)` made the dashboard cleaner and easier to understand while still showing the most important information.

### What I Learned

- A dashboard should explain important changes, not only display the latest values.
- Showing the severity transition makes classification decisions easier to review.
- Read-only reporting protects operational data while providing useful visibility.
- Clear presentation is just as important as accurate data.
- Small improvements to the output can make security information easier for analysts to understand.

### Next Expansion Scope or Idea

- Display assigned SOC analysts for active incidents.
- Show investigation duration and response time metrics.
- Add filtering by severity, status, or asset.
- Display security trends across multiple reporting periods.
- Export dashboard summaries to CSV or PDF reports.
