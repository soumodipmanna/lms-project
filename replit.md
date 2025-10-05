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
- Student signup and login with roll number authentication
- Book browsing dashboard
- Book borrow request system
- Admin approval workflow for borrow requests
- Book return tracking
- Student profile management (name and phone number)
- Django admin panel for managing books and students
- User avatar dropdown with logout functionality

## Recent Changes (October 5, 2025)

### Profile Management & Authentication Updates
1. **Student Model Enhancement**
   - Added `name` field (optional) for student's full name
   - Added `phone_number` field (optional) for contact information
   - Created migration 0010 to apply these changes

2. **Roll Number Authentication**
   - Changed login system to use roll number instead of username
   - Updated `StudentLoginForm` to accept roll_no field
   - Modified `student_login` view to authenticate using roll number

3. **Profile Management**
   - Created `manage_profile` view for students to update their information
   - Added `ProfileUpdateForm` allowing editing of name and phone_number only
   - Roll number and branch cannot be changed (read-only in profile)
   - Created profile management template with clean UI

4. **UI Enhancements**
   - Navbar now displays student's name if available, otherwise shows roll number
   - Added "Manage Profile" link to sidebar navigation
   - Moved logout to avatar dropdown menu in top right corner
   - Updated both dashboard and borrowed books templates

5. **Settings Configuration**
   - Added `LOGIN_URL = 'student_login'` to redirect unauthenticated users

### Replit Environment Setup
1. Installed Python 3.11 and Django 5.2.7
2. Configured Django settings for Replit:
   - Added CSRF_TRUSTED_ORIGINS for Replit domains
   - Set X_FRAME_OPTIONS to 'ALLOWALL' for iframe embedding
   - Added NoCacheMiddleware to prevent caching issues
3. Set up development workflow to run on port 5000 with 0.0.0.0 binding
4. Configured deployment with Gunicorn for production
5. Database migrations applied (SQLite)

## Technology Stack
- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **WSGI Server**: Gunicorn (production)
- **Python**: 3.11

## How to Use

### Student Login
Students now login using their **roll number** instead of username:
1. Navigate to `/login/`
2. Enter your roll number
3. Enter your password
4. Click "Sign In"

### Profile Management
Students can manage their profile information:
1. After logging in, click "Manage Profile" in the sidebar
2. Update your name and phone number
3. Click "Save Changes"
4. Roll number and branch cannot be changed

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
- `/login/` - Student login (using roll number)
- `/dashboard/` - Browse available books
- `/my-borrowed-books/` - View borrowed books
- `/manage-profile/` - Manage student profile
- `/admin/` - Django admin panel

## Database
Currently using SQLite for development. The database includes:
- **Book** model: title, author, ISBN, quantity
- **Student** model: user (OneToOne), roll_no, branch, name, phone_number
- **Borrow** model: student, book, dates, status, approval flags

## Deployment
Configured for Replit autoscale deployment using Gunicorn as the production WSGI server.

## User Preferences
None recorded yet.
