# Security Logic

## Why Asset Inventory Comes First

Security teams must know what assets exist before they can investigate vulnerabilities, incidents, or security risks.

Using a central asset inventory ensures every security event can be linked to the correct system, making investigations more accurate and consistent.

## Why IP Addresses Must Be Unique

The project prevents duplicate IP addresses because a single IP should represent one enterprise asset. This helps avoid inaccurate investigations and keeps asset records reliable.

## Why Asset Criticality Is Stored

Systems do not all have the same business importance. Storing asset criticality helps later components prioritise vulnerabilities and incidents based on their potential impact on the organisation.

## Why Vulnerabilities Are Linked to Assets

A vulnerability has limited investigation value without knowing which system it affects.

Linking vulnerabilities to enterprise assets helps analysts understand both the technical issue and the business impact.

## Why Vulnerabilities Are Ordered by Severity

Displaying Critical and High findings first helps security teams focus on the issues that require the fastest response.

## Why Duplicate Vulnerabilities Are Prevented

Duplicate findings can distort reports and make systems appear riskier than they actually are.

The project checks for existing vulnerability records before storing new ones.

## Why Risk Uses Multiple Factors

Asset criticality alone does not prove that a system is currently at critical risk.

Combining business importance, technical severity, and vulnerability count creates a more balanced assessment.

## Why the Highest Vulnerability Severity Is Used

The most severe known weakness represents the greatest immediate technical concern affecting an asset.

Additional vulnerabilities still increase the score through the vulnerability-count value.

## Why Risk Scores Are Recalculated

Risk can change when vulnerabilities are added, resolved, or reassessed.

Replacing previous scores ensures the table reflects the current security state instead of keeping outdated duplicate assessments.

## Why Scores Are Limited to 100

A consistent 0–100 range makes risk results easier to compare and prevents large vulnerability counts from producing uncontrolled values.

## Why Three Failed Logins Trigger Detection

A single failed login may be caused by a typing error, but repeated failures can indicate password guessing or brute-force activity.

The threshold is set to three attempts to provide early detection while avoiding alerts for most isolated login mistakes.

## Why Normal Events Are Reviewed but Not Stored as Incidents

Not every event requires an investigation record.

The detector reviews normal activity but creates an incident only when defined suspicious conditions are met, helping reduce unnecessary incident noise.

## Why Event Context Affects Detection

An action may be harmless in one situation but suspicious when combined with unusual time, location, network, or asset context.

Using several contextual factors produces more meaningful detections than evaluating the event type alone.

## Why Duplicate Incidents Are Prevented

Repeated processing of the same test data should not inflate incident counts or distort security reporting.

The detector checks the asset, incident type, source IP, and description before storing a new incident.

## Why Detection Severity Is Initial

The detector assigns a starting priority based on the information available when the event is detected.

The Severity Classification component can later confirm, increase, or reduce the priority after reviewing additional context.

## Why Severity Classification Uses Points

A point-based model provides a consistent way to combine the initial alert priority with the business risk of the affected asset.

The weights and thresholds remain visible, making classification decisions easier to explain, test, and tune.

## Why Initial Severity Is Preserved

The initial severity represents the detector's original assessment and should not change during later classification runs.

Keeping it separately prevents an already-escalated severity from being reused as the next starting value.

## Why Asset Risk Can Increase Severity

The same security event can have different consequences depending on the system it affects.

An event involving a high-risk or critical-risk asset may require faster investigation than the same event on a lower-risk system.

## Why Classification Reasons Are Stored

Analysts need to understand why an incident received its final priority.

Storing the contributing values supports auditing, troubleshooting, rule tuning, and false-positive analysis.

## Why Rules Should Be Tuned Carefully

A single false positive does not normally justify changing classification logic.

Rules should be adjusted after repeated patterns are confirmed and proposed changes are tested to ensure real attacks are not missed.

---

## Why Incident Timeline Management Is Used

An incident should follow a structured investigation process rather than being closed immediately after detection.

Recording each investigation stage creates a complete audit trail that shows what happened, who responded, and how the incident was handled.

## Why Incidents Follow a Fixed Lifecycle

Using the sequence Open → Investigating → Contained → Resolved ensures every incident is investigated, contained, and documented before it is closed.

A structured workflow also helps analysts taking over the investigation understand its current progress without reviewing every log from the beginning.

## Why Timeline Events Are Stored

Each timeline event records an important action during the investigation.

This provides historical evidence for auditing, reporting, compliance requirements, and post-incident reviews.

## Why Analyst Notes Are Recorded

Status changes alone do not explain why an incident progressed through each stage.

Recording analyst notes documents the investigation process and helps future analysts understand the actions already performed.

## Why Duplicate Timeline Events Are Prevented

The Incident Timeline component may be executed multiple times during testing or project validation.

Preventing duplicate timeline events keeps the investigation history accurate and avoids misleading reports.

## Why Investigation History Is Never Removed

Once an investigation event has been recorded, it becomes part of the permanent audit trail.

Keeping historical records supports compliance, forensic analysis, and lessons learned after an incident has been resolved.

## Why Current Incident Status Is Updated

Security teams need to know the latest investigation stage without reviewing every timeline event.

Updating the current incident status provides a quick view of whether an incident is Open, Investigating, Contained, or Resolved.

---

# Enterprise Dashboard Security Logic

## Why Use a Read-Only Dashboard?

The Enterprise Dashboard is designed to provide a consolidated view of the current security posture without changing any operational data. It only retrieves information from the database, ensuring that reporting activities cannot accidentally modify enterprise records.

---

## Why Display Enterprise Metrics?

Displaying the total number of assets, vulnerabilities, risk assessments, incidents, and timeline events gives analysts a quick overview of the environment before investigating individual incidents.

This reduces the need to query multiple database tables separately.

---

## Why Group Information by Risk and Severity?

Grouping incidents and assets by their current risk and severity helps analysts quickly identify where attention is needed.

Higher-risk assets and higher-severity incidents naturally receive higher priority during investigations.

---

## Why Display Priority Incidents?

Instead of reviewing every incident, the dashboard highlights the most important incidents first. This allows analysts to focus on higher-priority events before reviewing lower-risk activity.

---

## Why Show Severity Changes?

The dashboard displays both the initial severity and the final classified severity.

For example:

```
High -> Critical (Escalated)
```

This makes it easy to understand how the Severity Classification component changed the incident priority after considering asset risk.

It also helps analysts verify that the classification process is working as expected.

---

## Why Display Recent Timeline Activity?

Showing the latest investigation events allows analysts to immediately understand the most recent actions taken during incident response.

This provides useful operational context without opening the full investigation history.

---

## Security Benefit

The Enterprise Dashboard provides a single location to review the organisation's current security posture.

By combining information from multiple components into one read-only dashboard, analysts can quickly understand current risks, active incidents, and recent investigation activity while preserving the integrity of the enterprise database.
