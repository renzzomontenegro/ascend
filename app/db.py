import pymssql
from config import Config

def get_connection():
    return pymssql.connect(
        server=Config.SQL_SERVER,
        database=Config.SQL_DATABASE,
        user=Config.SQL_USERNAME,
        password=Config.SQL_PASSWORD
    )

def init_db():
    """Run once to create tables on Azure SQL."""
    conn = get_connection()
    cursor = conn.cursor()

    # Accounts table (admin + student logins)
    cursor.execute("""
        IF NOT EXISTS (
            SELECT * FROM sysobjects WHERE name='accounts' AND xtype='U'
        )
        CREATE TABLE accounts (
            id            INT IDENTITY PRIMARY KEY,
            username      VARCHAR(100) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            role          VARCHAR(20)  NOT NULL  -- 'student' or 'admin'
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

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialized.")