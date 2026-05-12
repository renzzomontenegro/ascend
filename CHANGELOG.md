# Changelog

All notable changes to this project will be documented in this file.

## [2026-05-12] - Project Setup 

### Added
- `Renzzo Montenegro` - Initialized GitHub repository `ascend`
- `Renzzo Montenegro` - Created full project folder structure: `/diagram`, `/deployment/screenshots`, `/report`, `/app`
- `Renzzo Montenegro` - Added root `README.md` with project overview and Azure services table
- `Renzzo Montenegro` - Added `CHANGELOG.md` following the given format
- `Jessica Lanuzo` - Added system diagram, `architecture.png` to diagram folder

### Changed
- `Renzzo Montenegro` - Updated root `README.md`

## [2026-05-12] - Application Development

### Added
- `Renzzo Montenegro` - Created Flask application backend with the following files:
  - `app/app.py` — all routes (register, login, logout, apply,
    status, admin dashboard, admin review)
  - `app/db.py` — Azure SQL connection helper and table
    initialization (accounts + enrollments tables)
  - `app/config.py` — environment variable management for
    Azure SQL, Blob Storage, and Application Insights
  - `app/requirements.txt` — initial project dependencies
  - `app/startup.sh` — gunicorn entry point for Azure App Service
  - `app/.env.example` — environment variable template
  - Added `.gitignore` at project root

### Changed
- `Renzzo Montenegro` - Replaced `pyodbc` with `pymssql` in `requirements.txt` and 
  `db.py` due to Microsoft C++ Build Tools compiler conflict on Windows 
- `Renzzo Montenegro` - Updated `config.py` connection string method to use
  `pymssql` dictionary format instead of `pyodbc` string format

### Fixed
- `Renzzo Montenegro` - Resolved `pyodbc` build error caused by missing/conflicting
  Microsoft Visual C++ 14.0 Build Tools
- `Renzzo Montenegro` - Resolved VS Code interpreter underline warnings by pointing
  IDE to correct venv Python interpreter
