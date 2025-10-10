# Library Management System (LMS)

## Overview
This Django-based Library Management System (LMS) facilitates book borrowing and management for students and administrators. Its primary purpose is to streamline the library's operations, offering students an intuitive platform to browse and request books, while providing administrators with robust tools for inventory management, user administration, and borrow request approvals. The system aims to enhance efficiency, reduce manual errors, and improve the overall library experience.

## User Preferences
None recorded yet.

## System Architecture
The LMS is built on Django 5.2.7 and utilizes a custom administrative portal alongside standard student-facing functionalities.

**UI/UX Decisions:**
- **Design Language**: iOS 26 liquid glass (glassmorphism) design system with frosted glass effects, translucent UI components, and modern blur aesthetics.
- **Theming**: Consistent purple gradient accents (#667eea to #764ba2) for active states and CTAs, complemented by book-themed loading animations.
- **Navigation**: Both student and admin interfaces feature sidebar navigation with identical glassmorphism styling, role-based menu items for administrators.
- **Navbar Design**: 
  - Admin/Student pages: Ultra-transparent glass appearance with 10% white translucent background (rgba(255,255,255,0.1))
  - Landing page: Ultra-transparent purple tint with 8% opacity (rgba(102,126,234,0.08))
  - All navbars: 20px backdrop blur with saturation boost, dark text (#333), subtle border effects
- **Sidebar Design**: 
  - 50% transparent white background (rgba(255,255,255,0.5)) with 20px backdrop blur and saturation effects
  - Smooth cubic-bezier animations (0.4s timing), rounded menu items with hover effects (translateX + accent bar)
  - Active state with purple gradient and white text, enhanced shadows for depth
  - When collapsed: 70px icon-only bar with centered icons, hidden text labels (using .icon and .label classes)
  - Toggle button icon changes dynamically: ☰ (hamburger) when expanded, → (arrow) when collapsed
  - Identical implementation across all admin and student pages
- **Search Bars**: iOS glass design with 60% translucent background, 20px blur/saturate filters, glass borders, 24px fully rounded corners (pill shape), smooth focus states with purple accent halos
- **Layout**: Clean, modern card-based layouts are used for dashboards and management pages.
- **Interactivity**: All pages include a collapsible sidebar toggled by a hamburger menu, with state persistence using localStorage. Smooth CSS transitions are used for animations.
- **Iconography**: An icon-based UI is used for actions like Edit (✏️), Delete (🗑️), Add (➕), Import (📥), Upload (⬆️), and Cancel (✖️) to enhance visual appeal and clarity.
- **Dashboard Cards**: Admin dashboard displays stat cards for Total Students (purple), Total Books (green), Pending Requests (orange), Fine Management (red, ₹), and Total Admins (blue, superadmin only).

**Technical Implementations & Feature Specifications:**
- **Authentication**:
    - **Student**: Uses roll number for login. Password hashing is handled by Django's utilities. Logout redirects to the home page.
    - **Admin**: Custom `Admin` model with email-based authentication. Two roles: 'officer' (manages students, books, requests) and 'superadmin' (manages other admins too). Custom decorators (`@admin_login_required`, `@superadmin_required`) enforce access control. Logout redirects to the home page.
- **User Management**:
    - **Student**: Signup creates account with 'pending' status requiring admin approval. Login checks status and shows rejection/disabled reasons. Profile management (name, phone number) and viewing borrowed books.
    - **Admin**: CRUD operations for students, books, and other admins (superadmin only).
- **Signup Approval Workflow**:
    - New student signups are set to 'pending' status by default
    - Admin "Signup Requests" page displays all pending signups
    - Admins can approve (one-click) or reject (with mandatory reason via modal) signup requests
    - Admins can disable existing active students (with mandatory reason via modal)
    - Student login enforces status checks: only 'approved' students can login
    - Rejected/disabled students see their status and reason when attempting login
    - Manually added or CSV-imported students are auto-approved
- **Book Management**:
    - Comprehensive CRUD for books, including fields for title, author, ISBN, quantity, category, department, language, and `fine_rate`.
    - CSV Bulk Import for students and books, with validation, duplicate handling, and sample CSV downloads.
- **Borrow Request Workflow**:
    - Students can request books and select an `expected_return_date` via a confirmation modal displaying fine rates.
    - Admins approve/reject requests. Rejection requires a `reject_reason`, which is displayed to students.
    - Admins can mark approved books as returned.
    - **Fine Calculation**: Automated calculation of `fine_amount` based on overdue days and the book's `fine_rate`. Fine amounts are displayed in Rupee (₹).
- **Error Handling & Validation**:
    - Server-side form validations for student signup, login, and admin login.
    - User-friendly error messages displayed inline and on the same page for authentication failures.
- **Core Models**:
    - `Book`: Includes `language`, `fine_rate`, `category`, and `department` fields for better organization.
    - `Student`: Linked to Django's `User` model, with `roll_no`, `branch`, `name`, `phone_number`, `status` (pending/approved/rejected/disabled), and `status_reason` (for rejection/disable explanations).
    - `Borrow`: Tracks student, book, dates, status, `expected_return_date`, `fine_amount`, and `reject_reason`.
    - `Admin`: Custom model with `email`, `password`, `name`, `role`, and `is_active`.

**System Design Choices:**
- **Development Environment**: Configured for Replit, running on port 5000 with `0.0.0.0` binding.
- **Deployment**: Utilizes Gunicorn as the WSGI server for production environments, configured for Replit autoscale deployment.
- **Database**: SQLite is used for development, with a structured schema including `Book`, `Student`, `Borrow`, and `Admin` models.
- **Currency**: All monetary values, specifically fine rates, are displayed in Indian Rupees (₹).
- **Caching**: Cache control headers (no-cache, no-store, must-revalidate) are implemented on the student dashboard to prevent browser caching issues with JavaScript functionality.
- **JavaScript Architecture**: Modal-related JavaScript functions are defined before HTML elements that reference them to ensure proper availability when inline onclick handlers execute.

## External Dependencies
- **Backend Framework**: Django 5.2.7
- **Database**: SQLite (for development)
- **WSGI Server**: Gunicorn (for production deployment)
- **Python Version**: 3.11