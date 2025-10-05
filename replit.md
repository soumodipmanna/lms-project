# Library Management System (LMS)

## Overview
This is a Django-based Library Management System that allows students to browse books, request to borrow them, and administrators to manage book inventory and approve borrow requests.

## Project Structure
- `lms_project/` - Django project root directory
  - `lms_project/` - Django configuration files (settings, URLs, WSGI)
  - `lms_app/` - Main application with models, views, templates
  - `db.sqlite3` - SQLite database
  - `manage.py` - Django management script

## Current Features
- Student signup and login
- Book browsing dashboard
- Book borrow request system
- Admin approval workflow for borrow requests
- Book return tracking
- Django admin panel for managing books and students

## Recent Changes (October 5, 2025)
### Replit Environment Setup
1. Installed Python 3.11 and Django 5.2.7
2. Configured Django settings for Replit:
   - Added CSRF_TRUSTED_ORIGINS for Replit domains
   - Set X_FRAME_OPTIONS to 'ALLOWALL' for iframe embedding
   - Added NoCacheMiddleware to prevent caching issues
3. Set up development workflow to run on port 5000 with 0.0.0.0 binding
4. Configured deployment with Gunicorn for production
5. Database migrations already applied (SQLite)

## Technology Stack
- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **WSGI Server**: Gunicorn (production)
- **Python**: 3.11

## How to Use

### Development
The development server is configured to run automatically on port 5000.

### Creating an Admin User
To access the Django admin panel, create a superuser:
```bash
cd lms_project
python manage.py createsuperuser
```

### Admin Panel
Access at `/admin/` to:
- Add/edit books
- Manage students
- Approve/reject borrow requests
- View all system data

### Available Routes
- `/` - Landing page
- `/signup/` - Student registration
- `/login/` - Student login
- `/dashboard/` - Browse available books
- `/my-borrowed-books/` - View borrowed books
- `/admin/` - Django admin panel

## Database
Currently using SQLite for development. The database includes:
- **Book** model: title, author, ISBN, quantity
- **Student** model: user (OneToOne), roll_no, branch
- **Borrow** model: student, book, dates, status, approval flags

## Deployment
Configured for Replit autoscale deployment using Gunicorn as the production WSGI server.

## User Preferences
None recorded yet.
