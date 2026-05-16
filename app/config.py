import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask
    SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "dev-secret-key")
    FLASK_ENV = os.environ.get("FLASK_ENV", "development")
    TEMPLATES_AUTO_RELOAD = True
    SEND_FILE_MAX_AGE_DEFAULT = 0

    # ── LOCAL DEV vs AZURE TOGGLE ──
    # Set USE_AZURE=true in .env to use Azure SQL + Blob Storage
    # Default (false) uses local SQLite + local file storage
    USE_AZURE = os.environ.get("USE_AZURE", "false").lower() == "true"
    DB_PATH = os.environ.get("DB_PATH", "app.db")  # SQLite path (dev only)

    # Azure SQL (production)
    SQL_SERVER   = os.environ.get("SQL_SERVER")
    SQL_DATABASE = os.environ.get("SQL_DATABASE")
    SQL_USERNAME = os.environ.get("SQL_USERNAME")
    SQL_PASSWORD = os.environ.get("SQL_PASSWORD")

    # Azure Blob Storage (production)
    AZURE_STORAGE_CONNECTION_STRING = os.environ.get("AZURE_STORAGE_CONNECTION_STRING")
    AZURE_BLOB_CONTAINER            = os.environ.get("AZURE_BLOB_CONTAINER", "documents")

    # Application Insights (production)
    APPINSIGHTS_KEY = os.environ.get("APPINSIGHTS_INSTRUMENTATIONKEY")

    @staticmethod
    def get_sql_connection_string():
        return {
            "server": Config.SQL_SERVER,
            "database": Config.SQL_DATABASE,
            "user": Config.SQL_USERNAME,
            "password": Config.SQL_PASSWORD,
            "tds_version": "7.4"
        }