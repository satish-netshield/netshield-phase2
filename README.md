...
## Asset Inventory

The Asset Inventory component stores and displays enterprise assets such as laptops, servers, and network devices.

Each asset includes:

- Asset name
- Asset type
- Department
- Owner
- Operating system
- IP address
- Criticality
- Operational status

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

## Vulnerability Tracking

The Vulnerability Tracking component records security weaknesses affecting known enterprise assets.

Each vulnerability includes:

- Related asset
- Vulnerability name
- CVE identifier (when available)
- Severity
- Description
- Status
- Discovery timestamp

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

- Four vulnerabilities were linked successfully to existing assets.
- Results were ordered by severity.
- Duplicate vulnerability records were prevented.
- Foreign-key validation prevented vulnerabilities from being linked to non-existent assets.
