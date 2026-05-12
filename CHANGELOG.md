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
- `Renzzo Montenegro` - Added setup instructions to README.md

### Fixed
- `Renzzo Montenegro` - Resolved `pyodbc` build error caused by missing/conflicting
  Microsoft Visual C++ 14.0 Build Tools
- `Renzzo Montenegro` - Resolved VS Code interpreter underline warnings by pointing
  IDE to correct venv Python interpreter

## [2026-05-13] - Initial Frontend & Local Dev

### Added
- `Jessica Lanuzo` - Added `app/templates/base.html` for the shared page layout, header, flash messages, and footer.
- `Jessica Lanuzo` - Added `app/static/css/style.css` for the first pass of page styling and responsive layout.
- `Jessica Lanuzo` - Added the first frontend template files for the app: `templates/index.html`, `templates/auth/login.html`, `templates/auth/register.html`, `templates/student/apply.html`, `templates/student/status.html`, `templates/admin/dashboard.html`, and `templates/admin/review.html`.
- `Jessica Lanuzo` - Added a `Run locally without Azure (dev mode)` section to the root `README.md` so the app can be run with SQLite and local uploads during development.

### Changed
- `Jessica Lanuzo` - Updated `app/app.py` to point to the new template folders in `auth/`, `student/`, and `admin/`, and to serve local uploads at `/uploads/<filename>` when `USE_AZURE=false`.
- `Jessica Lanuzo` - Added a `USE_AZURE` toggle and `DB_PATH` settings in `app/config.py` so the app can switch between SQLite for local dev and Azure SQL for production.
- `Jessica Lanuzo` - Updated `app/db.py` so it works with both SQLite and `pymssql`, including the small schema differences between the two.
- `Jessica Lanuzo` - Updated `.env.example` and `app/.env` to show the local dev values and the `USE_AZURE` setup.
- `Jessica Lanuzo` - Updated `.gitignore` to keep local dev files and sensitive files out of the repo, including `app/app.db`, `app/uploads/`, `app/.env`, and `.env`.

### Fixed
- `Jessica Lanuzo` - Added a local dev path that was missing from the earlier repo version, so the app can now be previewed without Azure credentials or cloud assets.
- `Jessica Lanuzo` - Documented the local preview flow to match the backend-first setup we started with before the frontend pages were added.
