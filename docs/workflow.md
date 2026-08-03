# Project Workflow

## Asset Inventory Workflow

### Workflow

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

### Component Inputs

- Asset information
- Enterprise database

### Component Processing

- Validates asset details.
- Prevents duplicate IP addresses.
- Stores asset information.
- Updates the enterprise inventory.
- Displays stored assets.

### Component Outputs

- Updated asset inventory.
- Stored enterprise assets.
- Current asset list.

### Security Purpose

The Asset Inventory provides the foundation for the NetShield Enterprise platform by maintaining an accurate record of enterprise assets that later components use for vulnerability management, risk assessment, and incident response.

---

## Vulnerability Tracking Workflow

### Workflow

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

### Component Inputs

- Existing enterprise assets.
- Vulnerability information.
- SQLite database.

### Component Processing

- Reads enterprise assets.
- Validates foreign-key relationships.
- Prevents duplicate vulnerabilities.
- Stores vulnerability records.
- Orders vulnerabilities by severity.

### Component Outputs

- Updated vulnerability inventory.
- Prioritised vulnerability list.

### Security Purpose

The Vulnerability Tracking component records security weaknesses against enterprise assets, allowing analysts to identify affected systems before calculating business risk.

---

## Risk Scoring Workflow

### Workflow

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

### Component Inputs

- Enterprise assets.
- Vulnerability inventory.

### Component Processing

- Reads asset information.
- Calculates risk points.
- Determines risk score.
- Assigns risk level.
- Stores current assessment.

### Component Outputs

- Risk scores.
- Risk levels.
- Risk assessment records.

### Security Purpose

The Risk Scoring Engine combines business importance with technical weaknesses to produce a consistent and explainable assessment of enterprise risk.

---

## Event Detection Workflow

### Workflow

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

### Component Inputs

- Simulated security events.
- Enterprise assets.
- Detection rules.

### Component Processing

- Reviews event context.
- Applies detection rules.
- Identifies suspicious activity.
- Creates incidents.
- Assigns initial severity.
- Prevents duplicate incidents.

### Component Outputs

- Security incidents.
- Initial severity.
- Incident records.

### Security Purpose

The Event Detection component transforms suspicious activity into security incidents while reducing alert noise by ignoring normal business activity.

---

## Severity Classification Workflow

### Workflow

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

### Component Inputs

- Open incidents.
- Asset risk scores.
- Initial severity.

### Component Processing

- Preserves original severity.
- Applies point-based scoring.
- Calculates classification score.
- Updates final severity.
- Stores classification reason.

### Component Outputs

- Updated incident severity.
- Classification reasons.
- Prioritised incidents.

### Security Purpose

The Severity Classification component combines detection results with business risk to produce a consistent and explainable incident priority.

---

## Incident Timeline Management Workflow

### Workflow

```text
Read Existing Incidents
        │
        ▼
Check Current Status
        │
        ▼
Create "Incident Detected" Timeline Event
        │
        ▼
Determine Next Investigation Stage
        │
        ▼
Update Incident Status
        │
        ▼
Store Analyst Notes
        │
        ▼
Prevent Duplicate Timeline Events
        │
        ▼
Save Timeline History
        │
        ▼
Display Investigation Timeline
```

### Component Inputs

- Incident records created by Event Detection.
- Final severity assigned by Severity Classification.
- Current incident status.
- Investigation workflow rules.

### Component Processing

- Reads existing incidents.
- Determines the next investigation stage.
- Creates timeline events.
- Updates incident status.
- Stores analyst notes.
- Prevents duplicate timeline events.
- Saves investigation history.

### Component Outputs

- Updated incident status.
- Timeline history.
- Analyst investigation notes.
- Complete audit trail.

### Security Purpose

The Incident Timeline Management component records every stage of the investigation lifecycle, creating a permanent audit trail that supports analyst handovers, compliance, reporting, and future investigations.
