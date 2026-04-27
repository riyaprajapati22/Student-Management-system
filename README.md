# 🎓 Student Management System

A full-stack web app to manage student records, marks, and attendance.
Built with **Python Flask + SQLite + HTML/CSS/JS**.

---

## 📁 Project Structure

```
student-management/
│
├── app.py                    ← Main Flask app (run this!)
├── requirements.txt          ← Python packages needed
├── README.md
│
├── database/
│   ├── __init__.py
│   ├── db_helper.py          ← All database functions
│   └── students.db           ← Auto-created on first run
│
├── templates/                ← HTML pages (Jinja2 templates)
│   ├── base.html             ← Master layout (sidebar + nav)
│   ├── login.html
│   ├── dashboard.html
│   ├── students.html
│   ├── add_student.html
│   ├── edit_student.html
│   ├── view_student.html
│   └── results.html
│
└── static/
    ├── css/
    │   ├── style.css         ← Global styles
    │   └── login.css         ← Login page styles
    └── js/
        └── main.js           ← Small JS utilities
```

---

## 🚀 How to Run (Step by Step)

### Step 1 — Make sure Python is installed
```bash
python --version
# Should show Python 3.8 or higher
```

### Step 2 — Open terminal in the project folder
```bash
cd student-management
```

### Step 3 — Install Flask
```bash
pip install flask
```

### Step 4 — Run the app
```bash
python app.py
```

### Step 5 — Open in browser
```
http://127.0.0.1:5000
```

---

## 🔐 Default Login

| Username | Password  |
|----------|-----------|
| admin    | admin123  |

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Admin Login** | Secure login with session management |
| **Dashboard** | Stats: total students, branches, avg marks, attendance |
| **Add Student** | Form with personal info, marks, attendance |
| **View Profile** | Full student profile with mark bars and grade |
| **Edit Student** | Update any student details |
| **Delete Student** | Remove student with confirmation |
| **Live Search** | Search by name or roll number (AJAX, no page reload) |
| **Results Page** | All students with subject-wise marks, grade, pass/fail |
| **Auto Grade** | Automatically calculates A+, A, B, C, D, F |
| **Sample Data** | 5 demo students loaded on first run |

---

## 🗃️ Database

Uses **SQLite** by default — no setup needed, file is auto-created.

To switch to **MySQL**, see instructions at the bottom of `database/db_helper.py`.

### Tables

**admins**
| Column | Type |
|--------|------|
| id | INTEGER |
| username | TEXT |
| password | TEXT |

**students**
| Column | Type |
|--------|------|
| id | INTEGER |
| name | TEXT |
| roll_no | TEXT (unique) |
| branch | TEXT |
| year | TEXT |
| email | TEXT |
| phone | TEXT |
| math | INTEGER |
| science | INTEGER |
| english | INTEGER |
| computers | INTEGER |
| attendance | INTEGER |
| created_at | TEXT |

---

## 📝 Resume Description

> **Student Management System**
> - Developed a full-stack web application to manage student records, attendance, and marks efficiently
> - Implemented add, update, delete, and live search functionalities using Flask and SQLite
> - Built an automatic grade and result calculator with a clean dashboard and analytics
> - Improved data organization through a user-friendly interface with responsive design

---

## 🔮 Ideas to Improve

- Add **multiple admin accounts** with roles (teacher, HOD, admin)
- Export results to **PDF or Excel**
- Add **charts** (bar chart of grade distribution)
- Add **subject-wise reports**
- Deploy on **Render.com** or **Railway.app** for free hosting

---

*Made with ❤️ as a college project*
