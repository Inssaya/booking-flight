 # booking-flight

Booking Flight is a Django web application for searching flights, viewing flight details, and booking seats online.
The project includes user authentication features (signup, login, profile management) and a custom admin-facing dashboard for managing airports, flights, and seats.

 # Owner

Yassine Sinif

 Features

- Search and browse available flights
- View flight details and seat options
- Book tickets and manage personal bookings
- User authentication (signup, login, logout, password reset)
- Profile page and profile edit
- Admin-facing dashboard for managing:
	- Airports
	- Flights
	- Seats

# Tech Stack

- Python
- Django 5.2.x
- SQLite (default database)

# Project Apps

- `accounts` for authentication and profile management
- `flights` for flight search, booking, and admin-facing flight management pages

# Quick Start (Windows)

1. Open terminal in project root:

```bat
cd "C:\Users\yassi\Desktop\2025\copy python-project\python-project"
```

2. Run server directly with venv Python (works without activation):

```bat
.\venv\Scripts\python.exe manage.py runserver
```

3. Open in browser:

```text
http://127.0.0.1:8000/
```

## Optional: Activate Virtual Environment

## PowerShell

```powershell
.\venv\Scripts\Activate.ps1
python manage.py runserver
```

## Command Prompt (cmd)

```bat
.\venv\Scripts\activate
python manage.py runserver
```

## Main Routes

- `/` home page (flight app)
- `/flights/` flight module routes
- `/accounts/` signup/login/profile routes
- `/admin/` default Django admin
- `/flights/admin/dashboard/` custom admin-facing dashboard in the flights app

## Notes

- Database file: `db.sqlite3`
- If you see a static files warning, create a `static` folder in project root.
- If Django is missing, make sure you are using the project virtual environment, not global Python.

