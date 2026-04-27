# ============================================================
#  db_helper.py  —  Database Helper
#  Uses SQLite by default (no extra setup needed!)
#  MySQL instructions at the bottom of this file.
# ============================================================

import sqlite3
import os

# Path to the database file
DB_PATH = os.path.join(os.path.dirname(__file__), "students.db")


class DatabaseHelper:

    def get_connection(self):
        """Create and return a database connection."""
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row   # makes rows behave like dictionaries
        return conn

    # ----------------------------------------------------------
    # INIT — Create tables if they don't exist
    # ----------------------------------------------------------
    def init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Admin table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id       INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT    NOT NULL UNIQUE,
                password TEXT    NOT NULL
            )
        """)

        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL,
                roll_no    TEXT    NOT NULL UNIQUE,
                branch     TEXT,
                year       TEXT,
                email      TEXT,
                phone      TEXT,
                math       INTEGER DEFAULT 0,
                science    INTEGER DEFAULT 0,
                english    INTEGER DEFAULT 0,
                computers  INTEGER DEFAULT 0,
                attendance INTEGER DEFAULT 0,
                created_at TEXT    DEFAULT (datetime('now'))
            )
        """)

        # Insert default admin (username: admin, password: admin123)
        cursor.execute("""
            INSERT OR IGNORE INTO admins (username, password)
            VALUES ('admin', 'admin123')
        """)

        # Insert some sample students so it's not empty on first run
        sample_students = [
            ("Rahul Sharma",   "101", "Computer Science", "2nd Year", "rahul@email.com",   "9876543210", 85, 78, 90, 92, 88),
            ("Priya Patel",    "102", "Information Tech", "2nd Year", "priya@email.com",   "9876543211", 92, 88, 85, 95, 95),
            ("Amit Kumar",     "103", "Electronics",      "1st Year", "amit@email.com",    "9876543212", 70, 75, 68, 72, 75),
            ("Sneha Joshi",    "104", "Computer Science", "3rd Year", "sneha@email.com",   "9876543213", 88, 92, 87, 90, 92),
            ("Rohan Verma",    "105", "Mechanical",       "1st Year", "rohan@email.com",   "9876543214", 60, 65, 58, 55, 70),
        ]

        cursor.executemany("""
            INSERT OR IGNORE INTO students
            (name, roll_no, branch, year, email, phone, math, science, english, computers, attendance)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, sample_students)

        conn.commit()
        conn.close()
        print("Database initialized successfully!")

    # ----------------------------------------------------------
    # AUTH
    # ----------------------------------------------------------
    def check_admin(self, username, password):
        """Return True if username + password match."""
        conn = self.get_connection()
        row = conn.execute(
            "SELECT * FROM admins WHERE username=? AND password=?",
            (username, password)
        ).fetchone()
        conn.close()
        return row is not None

    # ----------------------------------------------------------
    # STUDENTS — READ
    # ----------------------------------------------------------
    def get_all_students(self):
        """Return list of all students."""
        conn = self.get_connection()
        rows = conn.execute(
            "SELECT * FROM students ORDER BY roll_no"
        ).fetchall()
        conn.close()
        return [self._calculate_result(dict(row)) for row in rows]

    def get_student_by_id(self, student_id):
        """Return one student by ID."""
        conn = self.get_connection()
        row = conn.execute(
            "SELECT * FROM students WHERE id=?", (student_id,)
        ).fetchone()
        conn.close()
        if row:
            return self._calculate_result(dict(row))
        return None

    def search_students(self, query):
        """Search by name or roll number. Returns JSON-safe list."""
        conn = self.get_connection()
        rows = conn.execute(
            """SELECT * FROM students
               WHERE name LIKE ? OR roll_no LIKE ?
               ORDER BY roll_no""",
            (f"%{query}%", f"%{query}%")
        ).fetchall()
        conn.close()
        results = [self._calculate_result(dict(row)) for row in rows]
        return results

    def roll_exists(self, roll_no, exclude_id=None):
        """Check if a roll number already exists."""
        conn = self.get_connection()
        if exclude_id:
            row = conn.execute(
                "SELECT id FROM students WHERE roll_no=? AND id!=?",
                (roll_no, exclude_id)
            ).fetchone()
        else:
            row = conn.execute(
                "SELECT id FROM students WHERE roll_no=?", (roll_no,)
            ).fetchone()
        conn.close()
        return row is not None

    # ----------------------------------------------------------
    # STUDENTS — CREATE / UPDATE / DELETE
    # ----------------------------------------------------------
    def add_student(self, data):
        """Insert a new student. Returns True on success."""
        try:
            conn = self.get_connection()
            conn.execute("""
                INSERT INTO students
                (name, roll_no, branch, year, email, phone,
                 math, science, english, computers, attendance)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data["name"], data["roll_no"], data["branch"], data["year"],
                data["email"], data["phone"],
                int(data["math"]), int(data["science"]),
                int(data["english"]), int(data["computers"]),
                int(data["attendance"])
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Add error:", e)
            return False

    def update_student(self, data):
        """Update an existing student. Returns True on success."""
        try:
            conn = self.get_connection()
            conn.execute("""
                UPDATE students SET
                    name=?, roll_no=?, branch=?, year=?, email=?, phone=?,
                    math=?, science=?, english=?, computers=?, attendance=?
                WHERE id=?
            """, (
                data["name"], data["roll_no"], data["branch"], data["year"],
                data["email"], data["phone"],
                int(data["math"]), int(data["science"]),
                int(data["english"]), int(data["computers"]),
                int(data["attendance"]), data["id"]
            ))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            print("Update error:", e)
            return False

    def delete_student(self, student_id):
        """Delete a student by ID."""
        conn = self.get_connection()
        conn.execute("DELETE FROM students WHERE id=?", (student_id,))
        conn.commit()
        conn.close()

    # ----------------------------------------------------------
    # STATS FOR DASHBOARD
    # ----------------------------------------------------------
    def get_stats(self):
        """Return summary numbers for the dashboard."""
        conn = self.get_connection()

        total    = conn.execute("SELECT COUNT(*) FROM students").fetchone()[0]
        branches = conn.execute("SELECT COUNT(DISTINCT branch) FROM students").fetchone()[0]

        # Average marks
        avg_row = conn.execute("""
            SELECT AVG((math + science + english + computers) / 4.0) FROM students
        """).fetchone()[0]
        avg_marks = round(avg_row, 1) if avg_row else 0

        # Average attendance
        avg_att = conn.execute("SELECT AVG(attendance) FROM students").fetchone()[0]
        avg_attendance = round(avg_att, 1) if avg_att else 0

        conn.close()

        return {
            "total_students":   total,
            "total_branches":   branches,
            "avg_marks":        avg_marks,
            "avg_attendance":   avg_attendance,
        }

    # ----------------------------------------------------------
    # HELPER — Calculate grade and percentage
    # ----------------------------------------------------------
    def _calculate_result(self, student):
        """Add percentage and grade to a student dict."""
        marks = [
            student.get("math", 0),
            student.get("science", 0),
            student.get("english", 0),
            student.get("computers", 0),
        ]
        total      = sum(marks)
        percentage = round(total / 4, 1)

        if percentage >= 90:
            grade = "A+"
        elif percentage >= 80:
            grade = "A"
        elif percentage >= 70:
            grade = "B"
        elif percentage >= 60:
            grade = "C"
        elif percentage >= 40:
            grade = "D"
        else:
            grade = "F"

        student["total_marks"]  = total
        student["percentage"]   = percentage
        student["grade"]        = grade
        student["pass_fail"]    = "Pass" if percentage >= 40 else "Fail"

        return student


# ============================================================
# HOW TO USE MYSQL INSTEAD OF SQLITE
# ============================================================
# 1. Install: pip install mysql-connector-python
# 2. Replace get_connection() with:
#
#    import mysql.connector
#    def get_connection(self):
#        return mysql.connector.connect(
#            host="localhost",
#            user="root",
#            password="your_password",
#            database="student_db"
#        )
#
# 3. Change all ? placeholders to %s in SQL queries
# 4. Create database in MySQL: CREATE DATABASE student_db;
# ============================================================
