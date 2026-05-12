# Student Enrollment System — Azure Cloud Deployment

**Course:** CSEC 3 – Cloud Computing (Microsoft Azure)
**Term:** AY 2025–2026, 2nd Semester
**Team:** John Renzzo Montenegro & Jessica Mae Lanuzo

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

See `/diagram/architecture.png`

---

## Deployment

See `/deployment/README.md` for full step-by-step Azure Portal deployment guide.

---

## Cost Estimate

See `/report/cost-estimate.md`

---

## Changelog

See `CHANGELOG.md`

---

## Contributors

- **Renzzo** — Backend, Deployment, Autoscaling
- **Jessica** — Frontend, Database setup, Application Insights, Cost Report