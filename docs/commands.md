# Commands Reference

## Run Project Scripts

Run the database initialization:

```bash
python3 scripts/01_db_init.py
```

Run the Asset Inventory:

```bash
python3 scripts/02_asset_inventory.py
```

Run Vulnerability Tracking:

```bash
python3 scripts/03_vulnerability_tracker.py
```
---

## SQLite Commands

Show all tables:

```bash
sqlite3 data/enterprise.db ".tables"
```

View all assets:

```bash
sqlite3 data/enterprise.db "SELECT * FROM assets;"
```

Count stored assets:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM assets;"
```

View all vulnerabilities:

```bash
sqlite3 data/enterprise.db "SELECT * FROM vulnerabilities;"
```

Count stored vulnerabilities:

```bash
sqlite3 data/enterprise.db "SELECT COUNT(*) FROM vulnerabilities;"
```

Test foreign-key protection:

```bash
sqlite3 data/enterprise.db "PRAGMA foreign_keys = ON; INSERT INTO vulnerabilities (asset_id, vulnerability_name, severity, description) VALUES (999, 'Invalid Test Vulnerability', 'High', 'Foreign key test');"
```
---

## Git Commands

Check repository status:

```bash
git status
```

Stage all changes:

```bash
git add .
```

Create a commit:

```bash
git commit -m "commit message"
```

Push changes to GitHub:

```bash
git push
```

---

## Development Workflow

```text
Plan
  ↓
Build
  ↓
Run
  ↓
Test
  ↓
Update Documentation
  ↓
Review Documentation
  ↓
Git Commit
  ↓
Git Push
  ↓
Next Component
```
