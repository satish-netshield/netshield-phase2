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
