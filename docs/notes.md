## Database Initialization

The database initialization script creates the SQLite database used throughout the project.

It creates five core tables:

- Assets
- Vulnerabilities
- Incidents
- Risk Scores
- Incident Timeline

The database is created only if it does not already exist, allowing the script to be run multiple times safely.

### Notes from Testing

- Database created successfully.
- All five tables were verified using SQLite.
- Foreign key support is enabled by the application.

## Asset Inventory

The asset inventory script adds enterprise assets to the SQLite database and displays the current inventory.

The script uses parameterized SQL queries to insert data safely. It can be run multiple times without creating duplicate IP records.

### Notes from Testing

- Four sample assets were added successfully.
- The second run confirmed that duplicate IP addresses were blocked.
- Duplicate errors were replaced with clearer user-facing messages.
