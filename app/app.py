from flask import (Flask, render_template, request,
                   redirect, url_for, session, flash)
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from config import Config
from db import get_connection, init_db
import os

if Config.USE_AZURE:
    from azure.storage.blob import BlobServiceClient
    from applicationinsights.flask.ext import AppInsights

app = Flask(__name__)
app.config.from_object(Config)

# Application Insights (production only)
if Config.USE_AZURE and Config.APPINSIGHTS_KEY:
    appinsights = AppInsights(app)

# HELPERS

def upload_to_blob(file):
    """Upload a file to Azure Blob Storage (prod) or store locally (dev)."""
    if not file or not file.filename:
        return None

    filename = secure_filename(file.filename)

    if Config.USE_AZURE:
        # Production: upload to Azure Blob Storage
        client = BlobServiceClient.from_connection_string(
            Config.AZURE_STORAGE_CONNECTION_STRING
        )
        container = client.get_container_client(Config.AZURE_BLOB_CONTAINER)
        blob = container.get_blob_client(filename)
        blob.upload_blob(file.read(), overwrite=True)
        return blob.url
    else:
        # Development: save to local /uploads directory
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        os.makedirs(upload_dir, exist_ok=True)
        filepath = os.path.join(upload_dir, filename)
        file.save(filepath)
        return f"/uploads/{filename}"  # Return a relative URL

def login_required(role=None):
    """Decorator — protect routes by role."""
    from functools import wraps
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if "user_id" not in session:
                flash("Please log in first.", "warning")
                return redirect(url_for("login"))
            if role and session.get("role") != role:
                flash("Unauthorized access.", "danger")
                return redirect(url_for("index"))
            return f(*args, **kwargs)
        return wrapped
    return decorator

# PUBLIC ROUTES

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        conn = get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO accounts (username, password_hash, role) VALUES (?, ?, 'student')",
                (username, password)
            )
            conn.commit()
            flash("Account created! Please log in.", "success")
            return redirect(url_for("login"))
        except Exception:
            flash("Username already exists.", "danger")
        finally:
            cursor.close()
            conn.close()
    return render_template("auth/register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, password_hash, role FROM accounts WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        if user and check_password_hash(user[1], password):
            session["user_id"] = user[0]
            session["username"] = username
            session["role"]    = user[2]
            if user[2] == "admin":
                return redirect(url_for("admin_dashboard"))
            return redirect(url_for("apply"))
        flash("Invalid credentials.", "danger")
    return render_template("auth/login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully.", "success")
    return redirect(url_for("index"))

# STUDENT ROUTES

@app.route("/apply", methods=["GET", "POST"])
@login_required(role="student")
def apply():
    if request.method == "POST":
        student_name = request.form["student_name"]
        student_id   = request.form["student_id"]
        course       = request.form["course"]
        year_level   = request.form["year_level"]
        email        = request.form["email"]
        document     = request.files.get("document")
        document_url = None

        if document and document.filename:
            document_url = upload_to_blob(document)

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO enrollments
              (student_name, student_id, course, year_level,
               email, document_url, account_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (student_name, student_id, course,
              year_level, email, document_url, session["user_id"]))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Application submitted successfully!", "success")
        return redirect(url_for("status"))
    return render_template("student/apply.html")

@app.route("/status")
@login_required(role="student")
def status():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT student_name, course, year_level,
               status, submitted_at, admin_notes
        FROM enrollments
        WHERE account_id = ?
        ORDER BY submitted_at DESC
    """, (session["user_id"],))
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("student/status.html", applications=applications)

# ADMIN ROUTES

@app.route("/admin")
@login_required(role="admin")
def admin_dashboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, student_name, student_id, course,
               year_level, email, status, submitted_at
        FROM enrollments
        ORDER BY submitted_at DESC
    """)
    applications = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("admin/dashboard.html", applications=applications)

@app.route("/admin/review/<int:app_id>", methods=["GET", "POST"])
@login_required(role="admin")
def admin_review(app_id):
    conn = get_connection()
    cursor = conn.cursor()
    if request.method == "POST":
        status     = request.form["status"]
        admin_notes = request.form["admin_notes"]
        
        # Use appropriate SQL syntax for SQLite vs SQL Server
        if Config.USE_AZURE:
            sql = """
                UPDATE enrollments
                SET status = ?, admin_notes = ?, reviewed_at = GETDATE()
                WHERE id = ?
            """
        else:
            sql = """
                UPDATE enrollments
                SET status = ?, admin_notes = ?, reviewed_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """
        
        cursor.execute(sql, (status, admin_notes, app_id))
        conn.commit()
        flash(f"Application {status}.", "success")
        cursor.close()
        conn.close()
        return redirect(url_for("admin_dashboard"))

    cursor.execute("SELECT * FROM enrollments WHERE id = ?", (app_id,))
    application = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template("admin/review.html", application=application)

# SERVE UPLOADS (dev mode)
if not Config.USE_AZURE:
    import os.path
    @app.route('/uploads/<filename>')
    def uploaded_file(filename):
        from flask import send_from_directory
        upload_dir = os.path.join(os.path.dirname(__file__), "uploads")
        return send_from_directory(upload_dir, filename)

# ENTRY POINT

if __name__ == "__main__":
    init_db()
    debug_mode = not Config.USE_AZURE  # Debug=True for dev, False for prod
    print(f"Starting Flask app (USE_AZURE={Config.USE_AZURE}, DEBUG={debug_mode})")
    app.run(debug=debug_mode)