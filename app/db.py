import sqlite3
import os
from config import Config

if Config.USE_AZURE:
    import pymssql

def get_connection():
    """Get database connection — SQLite (dev) or Azure SQL (prod)."""
    if Config.USE_AZURE:
        # Production: Azure SQL
        return pymssql.connect(
            server=Config.SQL_SERVER,
            database=Config.SQL_DATABASE,
            user=Config.SQL_USERNAME,
            password=Config.SQL_PASSWORD
        )
    else:
        # Development: SQLite
        conn = sqlite3.connect(Config.DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

def init_db():
    """Create tables on SQLite (dev) or Azure SQL (prod)."""
    conn = get_connection()
    cursor = conn.cursor()

    if Config.USE_AZURE:
        # Azure SQL schema
        # Accounts table (admin + student logins)
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM sysobjects WHERE name='accounts' AND xtype='U'
            )
            CREATE TABLE accounts (
                id            INT IDENTITY PRIMARY KEY,
                username      VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role          VARCHAR(20)  NOT NULL
            )
        """)

        # Enrollments table
        cursor.execute("""
            IF NOT EXISTS (
                SELECT * FROM sysobjects WHERE name='enrollments' AND xtype='U'
            )
            CREATE TABLE enrollments (
                id            INT IDENTITY PRIMARY KEY,
                student_name  VARCHAR(100) NOT NULL,
                student_id    VARCHAR(50)  NOT NULL,
                course        VARCHAR(100) NOT NULL,
                year_level    VARCHAR(20)  NOT NULL,
                email         VARCHAR(100) NOT NULL,
                document_url  VARCHAR(500),
                status        VARCHAR(20)  DEFAULT 'Pending',
                submitted_at  DATETIME     DEFAULT GETDATE(),
                reviewed_at   DATETIME,
                admin_notes   VARCHAR(500),
                account_id    INT FOREIGN KEY REFERENCES accounts(id)
            )
        """)
    else:
        # SQLite schema (portable, no IDENTITY or GETDATE())
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                username      VARCHAR(100) NOT NULL UNIQUE,
                password_hash VARCHAR(255) NOT NULL,
                role          VARCHAR(20)  NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS enrollments (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                student_name  VARCHAR(100) NOT NULL,
                student_id    VARCHAR(50)  NOT NULL,
                course        VARCHAR(100) NOT NULL,
                year_level    VARCHAR(20)  NOT NULL,
                email         VARCHAR(100) NOT NULL,
                document_url  VARCHAR(500),
                status        VARCHAR(20)  DEFAULT 'Pending',
                submitted_at  DATETIME     DEFAULT CURRENT_TIMESTAMP,
                reviewed_at   DATETIME,
                admin_notes   VARCHAR(500),
                account_id    INTEGER REFERENCES accounts(id)
            )
        """)

    conn.commit()
    cursor.close()
    conn.close()
    db_type = "Azure SQL" if Config.USE_AZURE else "SQLite"
    print(f"Database initialized ({db_type}, {Config.DB_PATH if not Config.USE_AZURE else 'Azure'}).")