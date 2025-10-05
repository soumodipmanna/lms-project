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
- Book return tracking
- Student profile management (name and phone number)
- **Custom Admin Portal** with email-based authentication
- Role-based access control (Admin Officer & Superadmin)
- Complete CRUD operations for students, books, and admins
- Admin approval/rejection workflow for borrow requests
- **CSV Bulk Import** for students and books
- Loading animations on all pages with purple gradient theme
- User avatar dropdown with logout functionality

## Recent Changes (October 5, 2025)

### Fine Rate and Return Date System (Latest)
1. **Book Model Enhancement**
   - Added `language` field (max_length=50, default='English') for book language
   - Added `fine_rate` field (DecimalField, default=5.00) for variable daily fine rates per book
   - All 500 existing books set to language='English' and fine_rate=5.00 by default

2. **Borrow Model Enhancement**
   - Added `expected_return_date` field - students choose when borrowing
   - Added `fine_amount` field (DecimalField, default=0.00) to store calculated fines
   - Added `calculate_fine()` method that computes fine based on days overdue × book's fine_rate
   - Fine is automatically calculated and stored when book is returned late

3. **Borrow Workflow Updates**
   - **Modal Popup**: When borrowing, students see a confirmation modal displaying:
     - Book title and author
     - Fine rate per day (e.g., "$5.00/day if late")
     - Date picker to select expected return date
     - Warning message about late return fines
   - **Return Process**: When returning books:
     - Fine is calculated BEFORE marking as returned
     - Fine amount is stored in the database
     - Students see warning message: "Late return! Fine charged: $X.XX" if overdue
     - Or success message: "Book returned successfully!" if on-time

4. **CSV Import Updates**
   - CSV now accepts language and fine_rate columns (optional)
   - Updated CSV format: `title,author,isbn,quantity,category,department,language,fine_rate`
   - Sample CSV download includes example language and fine_rate values

5. **Admin Portal Updates**
   - Book management table displays Language and Fine/Day columns
   - Add/Edit book forms include language and fine_rate fields
   - Import books page shows updated CSV format with all fields

### Book Category and Department Fields
1. **Book Model Enhancement**
   - Added `category` field to Book model (max_length=100, default='dummy')
   - Added `department` field to Book model (max_length=100, default='dummy')
   - Created migration 0012 to apply these changes
   - All 500 existing books automatically set to category='dummy' and department='dummy'

2. **CSV Import Updates**
   - CSV import now accepts category and department columns
   - Fields are optional - default to 'dummy' if not provided

3. **Admin Portal Updates**
   - Book management table now displays Category and Department columns
   - Add/Edit book forms include category and department fields

4. **Purpose**
   - Enable future filtering of books by category (e.g., Programming, Literature)
   - Enable future filtering by department (e.g., Computer Science, Humanities)
   - Supports better book organization and search capabilities

### Collapsible Sidebar Feature
1. **All Pages Enhanced**
   - Added hamburger menu (☰) button to navbar on all admin and student pages
   - Click to toggle sidebar collapse/expand with smooth animations
   - Sidebar state persists using localStorage across page reloads
   - Smooth CSS transitions (0.3s ease) for all animations

### CSV Import Feature
1. **Student CSV Import**
   - Bulk upload students using CSV files
   - Required columns: username, password, roll_no, branch
   - Optional columns: email, name, phone_number
   - Automatically creates User accounts for each student
   - Validates data and skips duplicates
   - Displays success/error counts after import
   - **Download sample CSV** feature with pre-filled examples

2. **Book CSV Import**
   - Bulk upload books using CSV files
   - Required columns: title, author, isbn, quantity
   - Validates data and skips duplicates
   - Displays success/error counts after import
   - **Download sample CSV** feature with pre-filled examples

3. **UI Integration**
   - Import buttons added to Students and Books management pages
   - Import templates with CSV format instructions and download buttons
   - Loading animations during upload
   - Real-time success/error messaging
   - **Icon-based UI**: Edit (✏️), Delete (🗑️), Add (➕), Import (📥), Upload (⬆️), Cancel (✖️)
   - Enhanced visual appeal with icons throughout the admin portal

### Custom Admin Portal System (Latest)
1. **Admin Model**
   - Created custom Admin model with email authentication (no username)
   - Role field: 'officer' (manages students/books/requests) or 'superadmin' (can manage admins too)
   - Separate from Django's User model - uses session-based authentication
   - Password hashing using Django's password utilities

2. **Admin Authentication**
   - Email-only login (no admin signup - admins created by superadmins)
   - Custom decorators: @admin_login_required and @superadmin_required
   - Session stores admin_id, admin_name, and admin_role
   - Secure logout with session flush

3. **Admin Features**
   - Dashboard with statistics (total students, books, pending requests, admins)
   - Manage Students: list, add (with User creation), delete (with User cleanup)
   - Manage Books: list, add, edit, delete
   - Borrow Requests: list all requests, approve (decrements book quantity), reject
   - Manage Admins: list, add (superadmin only), delete (superadmin only, cannot delete self)

4. **UI/UX Design**
   - Purple gradient theme (#667eea to #764ba2) across all admin pages
   - Book-themed loading animations on all pages
   - Sidebar navigation with role-based menu items
   - Clean, modern card-based layouts
   - Real-time success/error messaging

5. **Test Account**
   - Superadmin: admin@library.com / admin123

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

### Admin Portal
Access the custom admin portal at `/admin-portal/login/` with these credentials:
- **Email**: admin@library.com
- **Password**: admin123

**Admin Officer Features:**
- Manage students (add individually, import via CSV, view, delete)
- Manage books (add individually, import via CSV, edit, delete)
- Review and approve/reject borrow requests

**Superadmin Additional Features:**
- All officer features
- Manage other admins (add, view, delete)
- Cannot delete themselves

### Available Routes

**Student Routes:**
- `/` - Landing page
- `/signup/` - Student registration
- `/login/` - Student login (using roll number)
- `/dashboard/` - Browse available books
- `/my-borrowed-books/` - View borrowed books
- `/manage-profile/` - Manage student profile

**Admin Portal Routes:**
- `/admin-portal/login/` - Admin login (email-based)
- `/admin-portal/dashboard/` - Admin dashboard with statistics
- `/admin-portal/students/` - Manage students
- `/admin-portal/students/import/` - Import students via CSV
- `/admin-portal/books/` - Manage books
- `/admin-portal/books/import/` - Import books via CSV
- `/admin-portal/borrow-requests/` - Review borrow requests
- `/admin-portal/admins/` - Manage admins (superadmin only)

## Database
Currently using SQLite for development. The database includes:
- **Book** model: title, author, ISBN, quantity, category, department, language, fine_rate
- **Student** model: user (OneToOne), roll_no, branch, name, phone_number
- **Borrow** model: student, book, dates, status, approval flags, expected_return_date, fine_amount
- **Admin** model: email, password, name, role (officer/superadmin), is_active

## Deployment
Configured for Replit autoscale deployment using Gunicorn as the production WSGI server.

## User Preferences
None recorded yet.
