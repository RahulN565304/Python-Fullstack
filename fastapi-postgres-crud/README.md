# Student Enrollment System API

A professional Full-Stack foundation project built using **FastAPI** and **PostgreSQL**. This project manages college students and their course enrollments using full **CRUD** operational architecture, built-in database validation shields, and cross-origin setup.

---

## 🛠️ Project Architecture & Tech Stack
* **Backend Framework:** FastAPI (Python)
* **Database Engine:** PostgreSQL
* **Data Validation:** Pydantic Models
* **Database Driver:** Psycopg2

---

## 🚀 Features Mastered

### 1. Full CRUD Database Operations
* **Create (POST):** Enrolls new students into existing database courses.
* **Read (GET):** Fetches student details using relational SQL `INNER JOIN` queries, with an active query parameter engine to search/filter records dynamically by course name.
* **Update (PUT):** Modifies a student's enrolled course cleanly using defensive logic.
* **Delete (DELETE):** Permanently purges a student record using path parameters.

### 2. Defensive Error Handling & Security Shields
* **Pydantic Guard:** Catches invalid input types (e.g., text instead of IDs) automatically before hitting the database.
* **Database Exceptions:** Gracefully manages relational database rules (like `ForeignKeyViolation` for missing course IDs) using localized `try/except` layers to prevent server crashes.
* **CORS Integration:** Configured using `CORSMiddleware` to authorize future web browser connections, laying the groundwork for upcoming frontend development.