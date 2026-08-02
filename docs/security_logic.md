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

