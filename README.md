# Library Management System (LMS)

A comprehensive web-based Library Management System built with Django, featuring book borrowing, student management, and a social knowledge-sharing wall.

## Features

### Student Portal
- **Book Browsing**: Browse and search available books by title, author, or ISBN
- **Borrow Requests**: Submit borrow requests with expected return dates
- **My Borrowed Books**: Track borrowed books, due dates, and fines
- **Profile Management**: Update personal information

### Knowledge Wall (Social Feature)
- **Post Sharing**: Share thoughts, ideas, and knowledge with fellow learners
- **Image Uploads**: Attach images to posts
- **Likes & Comments**: Interact with posts using heart-based likes and comments
- **Content Moderation**: Automatic filtering of inappropriate language
- **Delete Controls**: Users can delete own posts; admins can delete any post

### Admin Portal
- **Dashboard**: Overview of library statistics (students, books, pending requests, fines)
- **Student Management**: Add, approve, reject, or disable students
- **Book Management**: Add, edit, delete books with CSV import support
- **Borrow Requests**: Approve, reject, or mark books as returned
- **Admin Management**: Superadmins can manage other admin accounts

## Tech Stack

- **Backend**: Django 5.2
- **Database**: SQLite (default) / PostgreSQL compatible
- **Frontend**: HTML5, CSS3, JavaScript
- **Icons**: Font Awesome 6.4
- **Image Handling**: Pillow

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd lms_project
```

2. Install dependencies:
```bash
pip install django pillow gunicorn
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superadmin (optional):
```bash
python manage.py shell
```
```python
from lms_app.models import Admin
admin = Admin(email='admin@example.com', name='Admin', role='superadmin')
admin.set_password('yourpassword')
admin.save()
```

5. Run the development server:
```bash
python manage.py runserver 0.0.0.0:5000
```

## Project Structure

```
lms_project/
├── lms_app/
│   ├── migrations/
│   ├── templates/
│   │   ├── dashboard.html
│   │   ├── social_wall.html
│   │   ├── student_login.html
│   │   ├── student_signup.html
│   │   ├── admin_*.html
│   │   └── ...
│   ├── models.py          # Database models
│   ├── views.py           # View functions
│   ├── urls.py            # URL routing
│   ├── forms.py           # Form definitions
│   ├── moderation.py      # Content moderation
│   └── middleware.py      # Custom middleware
├── lms_project/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Main URL config
│   └── wsgi.py
├── media/                 # Uploaded images
└── manage.py
```

## Key Models

- **Student**: Library members with approval workflow
- **Book**: Library inventory with category, department, and fine rates
- **Borrow**: Book borrowing records with status tracking
- **Post**: Social wall posts with image support
- **Like**: Post likes (one per user per post)
- **Comment**: Post comments with moderation

## Security Features

- CSRF protection enabled
- Password hashing with Django's built-in hashers
- Content moderation for social features
- Role-based access control (Student, Admin Officer, Superadmin)
- Session-based authentication

## Fine System

- Configurable fine rates per book (in Rupees)
- Automatic fine calculation based on overdue days
- Fine tracking in borrow records

## Screenshots

The application features a modern, responsive UI with:
- Glassmorphism design elements
- Gradient accents
- Smooth animations and transitions
- Collapsible sidebar navigation

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
