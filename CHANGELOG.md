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
- `Renzzo Montenegro` - Replaced `pyodbc` with `pymssql` in `requirements.txt` and `db.py` due to Microsoft C++ Build Tools compiler conflict on Windows 
- `Renzzo Montenegro` - Updated `config.py` connection string method to use `pymssql` dictionary format instead of `pyodbc` string format
- `Renzzo Montenegro` - Added setup instructions to README.md

### Fixed
- `Renzzo Montenegro` - Resolved `pyodbc` build error caused by missing/conflicting Microsoft Visual C++ 14.0 Build Tools
- `Renzzo Montenegro` - Resolved VS Code interpreter underline warnings by pointing IDE to correct venv Python interpreter

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
- `Jessica Lanuzo` - Updated date rendering in `app/templates/admin/dashboard.html`, `app/templates/admin/review.html`, and `app/templates/student/status.html` to safely handle both datetime and string values, preventing template crashes (`'str' object has no attribute 'strftime'`) in local dev.

## [2026-05-13] - Azure Deployment and Credentials

### Added
- `Renzzo Montenegro` - Created Azure Resource Group `ascend-rg` (Region: East Asia)                  
  - (screenshot in deployment/screenshots/01)
- `Renzzo Montenegro` - Created Azure App Service Plan `ascend-plan` (Linux, F1 Free tier)            
  - (screenshot in deployment/screenshots/02)
- `Renzzo Montenegro` - Created Azure App Service `ascend-app` (Python 3.10, Linux)                   
  - (screenshot in deployment/screenshots/03)
- `Renzzo Montenegro` - Enabled Application Insights during App Service creation (`ascend-insights`)  
  - (screenshot in deployment/screenshots/04)
- `Renzzo Montenegro` - Configured HTTPS-only enforcement and TLS 1.2 minimum                         
  - (screenshot in deployment/screenshots/05)
- `Renzzo Montenegro` - Added all application environment variables to App Service Configuration      
  - (screenshot in deployment/screenshots/06)
- `Renzzo Montenegro` - Set gunicorn startup command for Flask production server                      
  - (screenshot in deployment/screenshots/07)
- `Jessica Lanuzo` - Created Azure SQL Server `ascend-sql-server` in East Asia (same region as other resources) in resource group `ascend-rg`
  - (screenshot in deployment/screenshots/6 and 7)
- `Jessica Lanuzo` - Created Azure SQL Database `enrollmentdb` in server `ascend-sql-server`
  - (screenshot in deployment/screenshots/11 to 22)
- `Jessica Lanuzo` - Created Blob Storage `ascend-storage` in East Asia in resource group `ascend-rg` with Standard performance and LRS redundancy
  - (screenshot in deployment/screenshots/24 to 28)
- `Jessica Lanuzo` - Created Blob Storage Container `documents` with Blob public access level in `ascend-storage`
  - (screenshot in deployment/screenshots/30 to 31)
  

### Changed
- `Jessica Lanuzo` - Configured `ascend-sql-server` firewall rules. Added client IP and allowed Azure service and resource access
  - (screenshot in deployment/screenshots/23)
- `Jessica Lanuzo` - Configured `ascendstorage` to enable anonymous access for public access blob container creation
  - (screenshot in deployment/screenshots/29)
- `Renzzo Montenegro` - Configured the SQL and Blob Storage connection settings as App Service environment variables with assistance from `Jessica`
- `Renzzo Montenegro` - Configured the App Insight Instrumentation Key on App Service Environment Variables

## [2026-05-13] - CI/CD and Deployment

### Added
- `Renzzo Montenegro` - Connected GitHub Actions CI/CD via Azure App Service Deployment Center
  - (screenshot in deployment/screenshots/08)
- `Renzzo Montenegro` - Azure auto-generated deployment workflow file linked to `main` branch of `ascend` repository
  - (screenshot in deployment/screenshots/09)
- `Renzzo Montenegro` - Verified live URL on Azure Portal
  - (screenshot in deployment/screenshots/10)

### Changed
- `Renzzo Montenegro` - Updated GitHub Actions CI/CD workflow `main_ascend-app.yml`

### Fixed
- `Renzzo Montenegro` - Corrected GitHub Actions CI/CD workflow `main_ascend-app.yml`

## [2026-05-13] - App Service Autoscale

### Added
- `Renzzo Montenegro` - Configured manual scale on App Service Plan `ascend-plan` (Basic B1, 2 active instances)
- `Renzzo Montenegro` - Set maximum scale instances to 3

### Notes
- Manual scaling chosen due to Azure for Students subscription onstraints (S1 at ~$56/month exceeds budget)
- Autoscale policy fully documented for production reference
- Cost saving: B1 vs S1 = ~$43/month reduction (77% savings)
- Full Rules-Based autoscaling requires Standard S1 tier

