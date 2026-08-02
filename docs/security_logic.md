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
