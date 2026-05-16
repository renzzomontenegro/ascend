# Student Enrollment System — Azure Cloud Deployment

**Course:** CSEC 3 – Cloud Computing (Microsoft Azure)
**Term:** AY 2025–2026, 2nd Semester
**Team:** John Renzzo Montenegro & Jessica Mae Lanuzo

Live Link: https://ascend-app-dfhbhdfcddewgdda.eastasia-01.azurewebsites.net/

Live Demo & Video Presentation: https://youtu.be/Ft73xUu7MQs

---

## Project Overview
ASCEND - Azure-based Student Cloud Enrollment Dashboard
- A web-based Student Enrollment System built with Python/Flask and deployed on Microsoft Azure. Students can submit enrollment applications, upload required documents, and track the status of their submissions (Pending, Approved, or Rejected). Administrators can review student submissions and approve or reject applications through an administrative dashboard. The system demonstrates cloud architecture, deployment, scalability, security, and monitoring using Azure services.

---

## Azure Services Used

| Service                                       | Purpose                                        |
|-----------------------------------------------|------------------------------------------------|
| Azure App Service                             | Hosts the Flask web application                |
| Azure SQL Database                            | Stores enrollment form submissions             |
| Azure Storage Account                         | Static assets and backup                       |
| Application Insights                          | Live monitoring and telemetry                  |
| App Service Autoscale                         | Automatic scaling based on CPU load            |

---

## Architecture

See `/diagram/architecture.png` for the full Azure architecture diagram.

**Services:**
- Azure App Service (Flask — Student + Admin Views)
- Azure SQL Database (Enrollment records, accounts)
- Azure Blob Storage (Student document uploads)

**Cloud Optimizations:**
- O1 — Autoscaling: scales out when CPU exceeds 70%
- O2 — Application Insights: live telemetry and error tracking
- O3 — GitHub Actions CI/CD: auto-deploy on push to main

**Security Controls:**
- HTTPS-only enforcement (TLS 1.2+)
- NSG rules (Port 443 inbound only)
- Azure SQL Firewall (App Service IP only)
- TDE — Transparent Data Encryption (at-rest)
- Session-based authentication (admin + student)
- Environment variables for all credentials (no hardcoding)

---

## Deployment

See `/deployment/README.md` for the full step-by-step
Azure Portal deployment guide with screenshots.

---

## Cost Estimate

See `/report/cost-estimate.md` for the full monthly
Azure cost breakdown and optimization strategies.

---

## Setup Instructions

### Prerequisites

Before running the project locally, make sure you have the following
installed on your machine:

- [Python 3.10+](https://www.python.org/downloads/)
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/) (recommended)
- [Azure Account](https://azure.microsoft.com/en-us/free/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/renzzomontenegro/ascend.git
cd ascend
```

---

### 2. Create and Activate Virtual Environment

```bash
cd app

# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

> You should see `(venv)` in your terminal prompt.

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure Environment Variables

Copy the example environment file and fill in your Azure credentials:

```bash
cp .env.example .env
```

Open `.env` and fill in the following values:

```env
USE_AZURE=true

# Azure SQL Database
SQL_SERVER=your-server-name.database.windows.net
SQL_DATABASE=enrollmentdb
SQL_USERNAME=your-sql-admin
SQL_PASSWORD=your-password

# Azure Blob Storage
AZURE_STORAGE_CONNECTION_STRING=your-connection-string
AZURE_BLOB_CONTAINER=documents

# Application Insights
APPINSIGHTS_INSTRUMENTATIONKEY=your-instrumentation-key

# Flask
FLASK_SECRET_KEY=your-random-secret-key
FLASK_ENV=development
```

> Never commit your `.env` file. It is already listed in `.gitignore`.

---

### 5. Initialize the Database

Run this once to create the required tables on your Azure SQL Database:

```bash
python db.py
```

> You should see: `Database initialized.`

---

### 6. Run the Application Locally

```bash
python app.py
```

Then open your browser and go to:
http://localhost:5000

---
## Run locally without Azure (Dev mode) — Quick local preview

**Quick:** preview and develop locally with SQLite and local file storage (no Azure required).

1. From the `app/` folder create and activate a virtual environment (recommended):

```bash
cd app
python -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\Scripts\activate   # Windows
```

2. Install dependencies (or use the minimal set for local dev):

```bash
pip install -r requirements.txt
# If you prefer a minimal install for quick preview:
pip install Flask==3.0.3 python-dotenv==1.0.1 werkzeug==3.0.3
```

3. Configure local environment variables. Copy the example and ensure `USE_AZURE` is false (default):

```bash
cp .env.example .env
# Edit .env and ensure:
# USE_AZURE=false
# DB_PATH=app.db   # optional
```

4. Initialize the local database (creates `app/app.db` and tables):

```bash
python -c "from db import init_db; init_db()"
```

5. (Optional) Create test accounts manually. You can create an admin and a student account using Python to generate a password hash and insert into the SQLite DB:

```bash
python - <<'PY'
from werkzeug.security import generate_password_hash
from db import get_connection
conn = get_connection()
cur = conn.cursor()
cur.execute("INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, ?)", ('admin', generate_password_hash('admin123'), 'admin'))
cur.execute("INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, ?)", ('student', generate_password_hash('student123'), 'student'))
conn.commit(); cur.close(); conn.close()
print('Created admin/student accounts: admin/admin123 and student/student123')
PY
```

Notes:
- The repository includes a helper `LOCAL_DEV.md` with the quick-start steps.
- In dev mode uploads are saved to `app/uploads/` and served at `/uploads/<filename>`.


---

### 7. Available Routes

| Route                | Access        | Description                   |
|----------------------|---------------|-------------------------------|
| `/`                  | Public        | Landing page                  |
| `/register`          | Public        | Student registration          |
| `/login`             | Public        | Student and admin login       |
| `/logout`            | Logged in     | Logout                        |
| `/apply`             | Student       | Submit enrollment form        |
| `/status`            | Student       | Track application status      |
| `/admin`             | Admin only    | View all submissions          |
| `/admin/review/<id>` | Admin only    | Approve or reject application |

---

### 8. Default Admin Account

To create an admin account, manually insert a record into the
`accounts` table in your Azure SQL Database:

```sql
INSERT INTO accounts (username, password_hash, role)
VALUES (
  'admin',
  '<hashed-password>',
  'admin'
);
```

To generate a hashed password, run this in Python:

```python
from werkzeug.security import generate_password_hash
print(generate_password_hash("your-admin-password"))
```

Copy the output and paste it as the `password_hash` value above.

---

## Repository Structure

```
ascend/
│
├── app/                          # Flask web application
│   ├── static/
│   │   └── style.css             # Global stylesheet
│   ├── templates/                # HTML templates
│   │   ├── base.html             # Shared base layout
│   │   ├── index.html            # Landing page
│   │   ├── login.html            # Login page
│   │   ├── register.html         # Student registration
│   │   ├── apply.html            # Enrollment form
│   │   ├── status.html           # Application status tracker
│   │   ├── admin_dashboard.html  # Admin — all submissions
│   │   └── admin_review.html     # Admin — approve/reject
│   ├── app.py                    # Main Flask application & routes
│   ├── config.py                 # Azure environment configuration
│   ├── db.py                     # Database connection & init
│   ├── requirements.txt          # Python dependencies
│   ├── startup.sh                # Gunicorn startup for App Service
│   └── .env.example              # Environment variable template
│
├── diagram/
│   └── architecture.png          # Azure architecture diagram
│
├── deployment/                   # Azure deployment documentation
│   ├── screenshots/              # Azure Portal screenshots
│   └── README.md                 # Step-by-step deployment guide
│
├── report/                       # Project reports
│   ├── cost-estimate.md          # Azure monthly cost breakdown
│   └── report.md                 # Full project report
│
├── .gitignore                    # Git ignored files
├── CHANGELOG.md                  # Project change history
└── README.md                     # Project overview & setup guide
```

---

## Changelog

See `CHANGELOG.md` for the full project history.

---

## Contributors

| Name        | Responsibilities                                                                                      |
|-------------|-------------------------------------------------------------------------------------------------------|
| **Renzzo**  | Backend (Flask routes, DB, config), Azure deployment, Autoscaling                                     |
| **Jessica** | Frontend (HTML templates), Azure SQL + Blob Storage setup, Application Insights, Cost Estimate Report |


## System Screenshots
- Landing page
![Ascend Landing Page](/deployment/screenshots/system-landing.png)
- Sign in, Register pages
![Ascend Login Page](/deployment/screenshots/system-sign-in.png)
![Ascend Register Page](/deployment/screenshots/system-register.png)

- Admin Views
![Ascend Admin View 1](/deployment/screenshots/system-admin-01.png)
![Ascend Admin View 2](/deployment/screenshots/system-admin-02.png)
- Student Views
![Ascend Student View 1](/deployment/screenshots/system-student-01.png)
![Ascend Student View 2](/deployment/screenshots/system-student-02.png)
