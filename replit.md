# Library Management System (LMS)

## Overview
A Django-based Library Management System with student and admin portals, plus a social "knowledge wall" feature.

## Tech Stack
- **Backend**: Django 5.2 (server-side rendered HTML)
- **Database**: SQLite (default)
- **Image handling**: Pillow
- **Server**: gunicorn (production), Django dev server (development)
- **Frontend**: HTML/CSS/JS templates with Font Awesome icons

## Project Structure
```
lms_project/
├── manage.py                    # Django management entry point
├── lms_project/
│   ├── settings.py              # Django settings
│   ├── urls.py                  # Root URL configuration
│   ├── wsgi.py                  # WSGI entry point
│   └── asgi.py                  # ASGI entry point
└── lms_app/
    ├── models.py                # Data models (Book, Borrow, Student, Admin, Post, etc.)
    ├── views.py                 # All view functions (student, admin, social wall)
    ├── urls.py                  # App URL routing
    ├── forms.py                 # Django forms
    ├── templates/               # HTML templates (admin_base.html is the shared base for all admin pages)
    ├── static/                  # Static assets (CSS, JS, images)
    ├── middleware.py             # NoCacheMiddleware
    ├── moderation.py            # Content filtering for social wall
    └── notifications.py         # Email notification helpers
```

## Key Routes
- `/` - Homepage
- `/signup/`, `/login/`, `/logout/` - Student authentication
- `/dashboard/` - Student dashboard
- `/my-borrowed-books/` - Student borrowed books
- `/admin-portal/login/` - Admin login
- `/admin-portal/dashboard/` - Admin dashboard
- `/social-wall/` - Social knowledge wall

## Running the App
The app runs via the "Server" workflow:
```
cd lms_project && python manage.py runserver 0.0.0.0:5000
```

## Authentication
Uses Django's built-in authentication system. Students sign up and are approved by admins. Admin accounts are managed separately.

## Email
Optional SMTP email (Mailgun) configured via environment variables. Falls back to console email backend when SMTP is not configured. Relevant env vars: `EMAIL_HOST_PASSWORD`, `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, `DEFAULT_FROM_EMAIL`.

## Database
SQLite database at `lms_project/db.sqlite3`. Migrations are managed via Django's migration system (`python manage.py migrate`).
