## Asset Inventory Workflow

```text
Start
  ↓
Receive Asset Information
  ↓
Validate Asset Details
  ↓
Store Asset in Enterprise Database
  ↓
Prevent Duplicate IP Addresses
  ↓
Update Asset Inventory
  ↓
Display Current Inventory
```

The Asset Inventory forms the foundation of the NetShield Enterprise platform.

---

## Vulnerability Tracking Workflow

```text
Select Existing Asset
  ↓
Receive Vulnerability Information
  ↓
Check for Existing Record
  ↓
Validate Asset Relationship
  ↓
Store Vulnerability
  ↓
Prioritise by Severity
  ↓
Display Vulnerability Inventory
```

Each vulnerability is linked to an existing enterprise asset, allowing analysts to identify the affected system before assessing risk.

---

## Risk Scoring Workflow

```text
Read Enterprise Assets
  ↓
Review Linked Vulnerabilities
  ↓
Identify Highest Vulnerability Severity
  ↓
Apply Asset Criticality Points
  ↓
Add Vulnerability Severity Points
  ↓
Add Vulnerability Count Points
  ↓
Calculate Overall Risk Score
  ↓
Assign Risk Level
  ↓
Store Current Risk Assessment
```

---

## Event Detection Workflow

```text
Receive Simulated Event
  ↓
Confirm Related Asset Exists
  ↓
Review Event Type and Context
  ↓
Apply Detection Rules
  ↓
Normal Activity?
  ├── Yes → Record as Reviewed Activity
  └── No  → Create Security Incident
                    ↓
           Assign Initial Severity
                    ↓
           Prevent Duplicate Detection
                    ↓
           Store Incident as Open
```

The detector uses asset importance, failed-attempt count, location, network type, and time context to distinguish normal activity from events requiring investigation.

---

## Severity Classification Workflow

```text
Read Open Incidents
  ↓
Preserve Initial Severity
  ↓
Read Related Asset Risk
  ↓
Convert Severity and Risk to Points
  ↓
Calculate Classification Score
  ↓
Assign Final Severity
  ↓
Store Classification Reason
  ↓
Update Current Incident Priority
```

The classifier uses the original detection severity and current asset risk to produce a consistent and explainable final priority.
