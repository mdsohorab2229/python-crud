# Student Management System (SMS) API

A lightweight **FastAPI** application for managing student records and their subject scores. Students and their English, Math, and History marks are persisted in a **MySQL** database through SQLAlchemy. Every student listing automatically includes the average-based performance comment, making this a small but complete example of a layered REST API (router → service → repository → model).

## Features

- **List students** — retrieve all students together with their subject scores and a computed performance comment (`Excellent` ≥ 90, `Better` ≥ 80, `Good` ≥ 70, otherwise `Need Improved`).
- **Create students** — add a student and the related score record in a single request (both `students` and `subjects` tables are populated).
- **Delete students** — remove a student by roll number along with the associated subject scores.
- **Partial updates** — update a student's name/email and/or any of the three subject scores via `PATCH`.
- **Request validation** — Pydantic models validate email format, name length (2–50 characters), and score ranges (0–100).
- **Automatic schema creation** — database tables are created on application startup.
- **Layered architecture** — clear separation of controllers, services, repositories, models, and schemas.
- **Interactive API docs** — auto-generated Swagger UI, ReDoc, and OpenAPI JSON.

## Tech Stack

| Layer | Technology |
| --- | --- |
| Language | Python 3 (project environment uses Python 3.15) |
| Web framework | [FastAPI](https://fastapi.tiangolo.com/) 0.163.2 |
| ASGI server | [Uvicorn](https://www.uvicorn.org/) 0.54.0 |
| Data validation | [Pydantic](https://docs.pydantic.dev/) 2.14.3 (with `email-validator` 2.4.0 for `EmailStr`) |
| ORM / database toolkit | [SQLAlchemy](https://www.sqlalchemy.org/) 2.1.9 |
| Database driver | [PyMySQL](https://pymysql.readthedocs.io/) 1.2.4 |
| Database | MySQL |
| Underlying ASGI toolkit | Starlette 1.10.0 |

All direct dependencies are declared in `requirements.txt`: `fastapi`, `uvicorn`, `pydantic`, `pymysql`, and `sqlalchemy`.

## Project Structure

```text
sms-fastapi/
├── main.py                          # FastAPI app, table creation, router registration
├── db.py                            # Engine, session factory, declarative base, DATABASE_URL
├── requirements.txt                 # Python dependencies
├── README.md                        # This documentation
├── model/
│   ├── student.py                   # Students ORM model (students table)
│   └── subject.py                   # Subjects ORM model (subjects table)
├── repository/
│   ├── student_repository.py        # Student database queries
│   └── course_repository.py         # Subject-score database queries
├── routers/
│   └── student_controller.py        # /students API routes
├── service/
│   └── student_service.py           # Business logic and grade-comment calculation
└── utils/
    └── schema.py                    # Pydantic request/response schemas
```

> Virtual environment (`.venv`/`venv`), `__pycache__`, `.git`, and IDE metadata are intentionally omitted from this tree.

## Installation & Local Setup

1. **Clone or open the project directory**

   ```bash
   cd sms-fastapi
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**

   Windows (Command Prompt):

   ```bat
   venv\Scripts\activate
   ```

   Windows (PowerShell):

   ```powershell
   venv\Scripts\Activate.ps1
   ```

   Linux / macOS:

   ```bash
   source venv/bin/activate
   ```

   > The existing local environment is named `.venv`; either name works as long as you activate the one you create.

4. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

5. **Prepare the database**

   Ensure a MySQL server is running and create the schema used by the application:

   ```sql
   CREATE DATABASE sms;
   ```

   Adjust host, port, user, and password as needed (see Environment Variables).

## Environment Variables

The database connection is currently defined directly in `db.py`:

```python
DATABASE_URL = "mysql+pymysql://root:@localhost:3307/sms"
```

No `.env` loader is bundled, so to externalize the configuration add `python-dotenv` (`pip install python-dotenv`) and load it in `db.py` with `load_dotenv()` before reading `os.getenv("DATABASE_URL")`.

Example `.env` file (dummy values):

```dotenv
# Database connection string: dialect+driver://user:password@host:port/database
DATABASE_URL=mysql+pymysql://root:root@localhost:3307/sms

# Optional server settings
HOST=127.0.0.1
PORT=8000
```

Suggested `db.py` change:

```python
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv(
    "DATABASE_URL", "mysql+pymysql://root:root@localhost:3307/sms"
)
```

| Variable | Description | Example |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy MySQL connection string | `mysql+pymysql://root:root@localhost:3307/sms` |
| `HOST` | Uvicorn bind address (optional) | `127.0.0.1` |
| `PORT` | Uvicorn port (optional) | `8000` |

## Running the Server

Start the development server with auto-reload:

```bash
uvicorn main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. To bind explicitly to all interfaces or a custom port:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## API Endpoints & Documentation

Base prefix: `/students`

| Method | Endpoint | Description |
| --- | --- | --- |
| `GET` | `/students/all` | Returns every student with subject scores and the computed performance comment (`200 OK`). |
| `POST` | `/students/add` | Creates a student and the corresponding subject-score record (`201 Created`). |
| `DELETE` | `/students/delete/{student_roll}` | Deletes the student and their subject scores by roll number (`204 No Content`). |
| `PATCH` | `/students/update/{student_roll}` | Partially updates name, email, and/or subject scores by roll number (`200 OK`). |

Example `POST /students/add` body:

```json
{
  "name": "Alice Khan",
  "age": 20,
  "email": "alice@example.com",
  "roll": 101,
  "session": "2024-2025",
  "department": "Computer Science",
  "english_score": 88,
  "math_score": 92,
  "history_score": 79
}
```

Example `PATCH /students/update/101` body (only the fields to change):

```json
{
  "name": "Alice Rahman",
  "math_score": 95
}
```

### Interactive Documentation

| Documentation | URL |
| --- | --- |
| Swagger UI | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |
| ReDoc | [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc) |
| OpenAPI schema | [http://127.0.0.1:8000/openapi.json](http://127.0.0.1:8000/openapi.json) |

Both `/docs` and `/redoc` let you inspect and try out every endpoint directly from the browser.
