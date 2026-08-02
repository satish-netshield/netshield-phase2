## Asset Inventory

The Asset Inventory component stores and displays enterprise assets such as laptops, servers, and network devices.

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

The classifier uses a transparent point-based model.

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
