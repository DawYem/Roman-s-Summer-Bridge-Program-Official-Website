from flask import Flask, render_template, request, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from io import BytesIO
from datetime import datetime
from werkzeug.utils import secure_filename


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        is_admin INTEGER NOT NULL DEFAULT 0
    )
""")
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS volunteer_hours (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        hours REAL NOT NULL,
        task TEXT NOT NULL,
        date TEXT NOT NULL,
        image TEXT
    )
""")
    conn.commit()
    conn.close()
     
app = Flask(__name__)
app.secret_key = "hedaredbro12467"

UPLOAD_FOLDER = "static/uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def has_first_and_last_name(name):
    parts = [part for part in name.split() if part]
    return len(parts) >= 2


@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route("/")
def home():
    return render_template ("home.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username:
            return render_template(
                "signup.html",
                error="First and last name cannot be empty.",
                signup_username=username
            )

        if not has_first_and_last_name(username):
            return render_template(
                "signup.html",
                error="Please enter both first and last name.",
                signup_username=username
            )

        hashed_password = generate_password_hash(password)
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT 1 FROM users WHERE LOWER(username) = LOWER(?)",
            (username,)
        )
        existing_user = cursor.fetchone()
        if existing_user:
            conn.close()
            return render_template(
                "signup.html",
                error="That name is already registered. Please log in.",
                signup_username=username
            )
        
        # Check if this is the first user
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        is_admin = 1 if user_count == 0 else 0
        
        cursor.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            (username, hashed_password, is_admin)
        )
        conn.commit()
        conn.close()
        return redirect(url_for("login"))
    return render_template("signup.html", signup_username="")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method =="POST":
        username = request.form["username"].strip()
        password = request.form["password"]

        if not username or not password:
            return render_template(
                "login.html",
                error="Please enter both username and password.",
                login_username=username
            )
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username=?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user[2], password):
            session["username"] = username
            return redirect(url_for("dashboard"))
        else:
            return render_template(
                "login.html",
                error="Invalid username or password.",
                login_username=username
            )
        
    return render_template("login.html", login_username="")

@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "username" not in session:
        return redirect(url_for("login"))

    username = session["username"]

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT is_admin FROM users WHERE username=?",
        (username,)
    )
    admin_row = cursor.fetchone()
    is_admin = bool(admin_row and admin_row[0] == 1)

    if request.method == "POST":
        hours = request.form["hours"]
        task = request.form["task"]
        date = request.form["date"]

        image_file = request.files.get("image")

        filename = None
        if image_file and image_file.filename != "":
            filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(image_path)

        cursor.execute(
            "INSERT INTO volunteer_hours (username, hours, task, date, image) VALUES (?, ?, ?, ?, ?)",
            (username, hours, task, date, filename)
        )
        conn.commit()

    if is_admin:
        cursor.execute(
            "SELECT username, hours, task, date, image FROM volunteer_hours ORDER BY date DESC"
        )
    else:
        cursor.execute(
            "SELECT username, hours, task, date, image FROM volunteer_hours WHERE username=? ORDER BY date DESC",
            (username,)
        )
    records = cursor.fetchall()

    conn.close()

    return render_template(
        "dashboard.html",
        username=username,
        records=records,
        is_admin=is_admin,
        show_all_submissions=is_admin
    )

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT is_admin FROM users WHERE username = ?",
        (session["username"],)
    )
    result = cursor.fetchone()

    if not result or result[0] != 1:
        conn.close()
        return "Access denied"

    cursor.execute("""
        SELECT username, hours, task, date, image
        FROM volunteer_hours
        ORDER BY date DESC
    """)
    all_records = cursor.fetchall()

    cursor.execute(
        "SELECT username, is_admin FROM users ORDER BY username"
    )
    users = cursor.fetchall()

    conn.close()

    return render_template("admin.html", records=all_records, users=users)

@app.route("/toggle_admin/<username>")
def toggle_admin(username):
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    # check current user is admin
    cursor.execute(
        "SELECT is_admin FROM users WHERE username = ?",
        (session["username"],)
    )
    current_user = cursor.fetchone()

    if not current_user or current_user[0] != 1:
        conn.close()
        return "Access denied"

    # ❗ prevent removing yourself
    if username == session["username"]:
        conn.close()
        return "You cannot change your own admin status"

    # toggle admin
    cursor.execute(
        "UPDATE users SET is_admin = NOT is_admin WHERE username = ?",
        (username,)
    )

    conn.commit()
    conn.close()

    return redirect(url_for("admin"))


@app.route("/admin/export")
def export_volunteer_data():
    if "username" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT is_admin FROM users WHERE username = ?",
        (session["username"],)
    )
    current_user = cursor.fetchone()

    if not current_user or current_user[0] != 1:
        conn.close()
        return "Access denied"

    cursor.execute(
        "SELECT username, hours, task, date, image FROM volunteer_hours ORDER BY date DESC"
    )
    records = cursor.fetchall()
    conn.close()

    try:
        from openpyxl import Workbook
    except ImportError:
        return "Excel export requires openpyxl. Install it with: pip install openpyxl"

    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Volunteer Submissions"

    headers = ["Username", "Hours", "Task", "Date", "Image File"]
    worksheet.append(headers)

    for row in records:
        worksheet.append(list(row))

    for column in worksheet.columns:
        max_length = 0
        column_letter = column[0].column_letter
        for cell in column:
            cell_value = "" if cell.value is None else str(cell.value)
            if len(cell_value) > max_length:
                max_length = len(cell_value)
        worksheet.column_dimensions[column_letter].width = min(max_length + 2, 40)

    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    file_name = f"volunteer_submissions_{datetime.now().strftime('%Y%m%d')}.xlsx"
    return send_file(
        output,
        as_attachment=True,
        download_name=file_name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

if __name__ == "__main__":
    init_db()
    app.run(debug = True)
