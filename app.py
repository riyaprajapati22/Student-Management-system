# ============================================================
#  app.py  —  Main Flask Application
#  Student Management System
#  Run this file to start the server: python app.py
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from database.db_helper import DatabaseHelper
from functools import wraps

app = Flask(__name__)

# Secret key for sessions (keep this secret in real projects!)
app.secret_key = "student_mgmt_secret_123"

# Create database helper instance
db = DatabaseHelper()


# ============================================================
# LOGIN REQUIRED DECORATOR
# Protects routes — redirects to login if not logged in
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if "admin" not in session:
            flash("Please login first.", "warning")
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated


# ============================================================
# ROUTE: Login Page
# ============================================================
@app.route("/", methods=["GET", "POST"])
@app.route("/login", methods=["GET", "POST"])
def login():
    # If already logged in, go to dashboard
    if "admin" in session:
        return redirect(url_for("dashboard"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "").strip()

        # Check credentials
        if db.check_admin(username, password):
            session["admin"] = username
            flash("Welcome back, " + username + "!", "success")
            return redirect(url_for("dashboard"))
        else:
            flash("Wrong username or password!", "danger")

    return render_template("login.html")


# ============================================================
# ROUTE: Logout
# ============================================================
@app.route("/logout")
def logout():
    session.pop("admin", None)
    flash("Logged out successfully.", "info")
    return redirect(url_for("login"))


# ============================================================
# ROUTE: Dashboard (Home)
# ============================================================
@app.route("/dashboard")
@login_required
def dashboard():
    stats = db.get_stats()
    return render_template("dashboard.html", stats=stats, admin=session["admin"])


# ============================================================
# ROUTE: All Students
# ============================================================
@app.route("/students")
@login_required
def students():
    all_students = db.get_all_students()
    return render_template("students.html", students=all_students)


# ============================================================
# ROUTE: Search Students (AJAX)
# ============================================================
@app.route("/search")
@login_required
def search():
    query = request.args.get("q", "").strip()
    results = db.search_students(query)
    return jsonify(results)


# ============================================================
# ROUTE: Add Student
# ============================================================
@app.route("/add", methods=["GET", "POST"])
@login_required
def add_student():
    if request.method == "POST":
        data = {
            "name":       request.form.get("name", "").strip(),
            "roll_no":    request.form.get("roll_no", "").strip(),
            "branch":     request.form.get("branch", "").strip(),
            "year":       request.form.get("year", "").strip(),
            "email":      request.form.get("email", "").strip(),
            "phone":      request.form.get("phone", "").strip(),
            "math":       request.form.get("math", 0),
            "science":    request.form.get("science", 0),
            "english":    request.form.get("english", 0),
            "computers":  request.form.get("computers", 0),
            "attendance": request.form.get("attendance", 0),
        }

        # Basic validation
        if not data["name"] or not data["roll_no"]:
            flash("Name and Roll Number are required!", "danger")
            return render_template("add_student.html")

        # Check if roll number already exists
        if db.roll_exists(data["roll_no"]):
            flash("Roll Number " + data["roll_no"] + " already exists!", "danger")
            return render_template("add_student.html")

        success = db.add_student(data)
        if success:
            flash("Student " + data["name"] + " added successfully!", "success")
            return redirect(url_for("students"))
        else:
            flash("Error adding student. Try again.", "danger")

    return render_template("add_student.html")


# ============================================================
# ROUTE: View Student Profile
# ============================================================
@app.route("/student/<int:student_id>")
@login_required
def view_student(student_id):
    student = db.get_student_by_id(student_id)
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("students"))
    return render_template("view_student.html", student=student)


# ============================================================
# ROUTE: Edit Student
# ============================================================
@app.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):
    student = db.get_student_by_id(student_id)
    if not student:
        flash("Student not found!", "danger")
        return redirect(url_for("students"))

    if request.method == "POST":
        data = {
            "id":         student_id,
            "name":       request.form.get("name", "").strip(),
            "roll_no":    request.form.get("roll_no", "").strip(),
            "branch":     request.form.get("branch", "").strip(),
            "year":       request.form.get("year", "").strip(),
            "email":      request.form.get("email", "").strip(),
            "phone":      request.form.get("phone", "").strip(),
            "math":       request.form.get("math", 0),
            "science":    request.form.get("science", 0),
            "english":    request.form.get("english", 0),
            "computers":  request.form.get("computers", 0),
            "attendance": request.form.get("attendance", 0),
        }

        success = db.update_student(data)
        if success:
            flash("Student updated successfully!", "success")
            return redirect(url_for("view_student", student_id=student_id))
        else:
            flash("Error updating student.", "danger")

    return render_template("edit_student.html", student=student)


# ============================================================
# ROUTE: Delete Student
# ============================================================
@app.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):
    student = db.get_student_by_id(student_id)
    if student:
        db.delete_student(student_id)
        flash("Student " + student["name"] + " deleted.", "info")
    return redirect(url_for("students"))


# ============================================================
# ROUTE: Results Summary
# ============================================================
@app.route("/results")
@login_required
def results():
    all_students = db.get_all_students()
    return render_template("results.html", students=all_students)


# ============================================================
# START THE APP
# ============================================================
if __name__ == "__main__":
    # Create tables if they don't exist
    db.init_db()
    print("=" * 50)
    print("  Student Management System Running!")
    print("  Open: http://127.0.0.1:5000")
    print("  Admin Login: admin / admin123")
    print("=" * 50)
    app.run(debug=True)
