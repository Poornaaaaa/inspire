# Inspire 2026 - Django REST Backend Integration & Setup Guide

This document provides complete instructions for running, testing, and managing the **Django REST API Backend** connected to the **Inspire 2026** Fest website and scoring system.

---

## 🏗️ Architecture Overview

The system operates with a multi-layered sync architecture:

1. **Django REST Framework API (`inspire_backend`)**:
   - Live SQLite/PostgreSQL Database storing:
     - 11 Official Competing Squads (with live point tallies & baseline 0 PTS).
     - 14 Official Competition Tracks.
     - Student Delegate Registrations (with unique Pass IDs).
     - Admin Score Audit Logs.
   - Cross-Origin Resource Sharing (`django-cors-headers`) enabled for seamless connection from `index.html` and `admin.html`.
2. **Frontend Applications**:
   - `index.html`: Public fest website (live leaderboard, podium, mobile navigation, registration modal).
   - `admin.html`: Fest Coordinator scoring console & points distribution engine.
3. **Google Cloud / Sheets (Redundant Fallback)**:
   - If the local Django server is temporarily offline, the frontend gracefully falls back to Google Cloud Web App synchronization without any disruption to users.

---

## 🚀 Quick Start (Local Development)

### 1. Requirements
Ensure Python 3.10+ is installed on your machine.

### 2. Navigate to the Backend Directory
```bash
cd inspire_backend
```

### 3. Install Required Dependencies
```bash
pip install -r requirements.txt
```
*(Dependencies: `Django>=5.0`, `djangorestframework>=3.14.0`, `django-cors-headers>=4.3.0`)*

### 4. Run Migrations & Seed Initial Data
```bash
python manage.py makemigrations api
python manage.py migrate
python manage.py seed_inspire_data
```

### 5. Create an Admin Superuser (Optional for Django `/admin/` portal)
```bash
python manage.py createsuperuser
```

### 6. Start the Django Server
```bash
python manage.py runserver 127.0.0.1:8000
```

Once running, your API is active at `http://127.0.0.1:8000/api/`.

---

## 📡 REST API Reference

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/scores/` | `GET` | Live standings of all 11 competing squads (sorted by PTS). |
| `/api/scores/update/` | `POST` | Update points for single squad or batch squads. |
| `/api/scores/reset/` | `POST` | Reset all 11 squad points back to zero (0 PTS). |
| `/api/register/` | `POST` | Register a delegate/team and receive ticket confirmation. |
| `/api/registrations/` | `GET` | List registrations with optional filtering (`?event=...`, `?squad=...`, `?search=...`). |
| `/api/admin/login/` | `POST` | Authenticate Fest Admin credentials (`admin` / `Poorna@292004`). |
| `/api/events/` | `GET` | Retrieve the 14 official competition tracks. |
| `/admin/` | `GET` | Django GUI Administration dashboard. |

---

## 🧪 Running Automated API Tests

To verify that all database operations, serializers, and endpoints work correctly:

```bash
cd inspire_backend
python manage.py test api
```

Expected Output:
```
Ran 4 tests in 0.144s
OK
```

---

## 🌐 Production Deployment (Gunicorn / Render / Railway / AWS / VPS)

### Production Settings in `inspire_project/settings.py`
1. Set `DEBUG = False`
2. Set `ALLOWED_HOSTS = ['yourdomain.com', 'localhost', '127.0.0.1']`
3. Update `CORS_ALLOWED_ORIGINS` to include your production frontend domain (e.g. `https://yourfestdomain.com`).

### Serving with Gunicorn
```bash
pip install gunicorn
gunicorn inspire_project.wsgi:application --bind 0.0.0.0:8000
```
