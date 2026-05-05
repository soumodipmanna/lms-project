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

## Run with Docker

The repo includes a `Dockerfile` and `docker-compose.yml` so you can build and run the whole app in one command:

```bash
docker compose up --build
```

Then open http://localhost:5000.

Configuration (optional): copy `.env.example` to `.env` and adjust values such as `DJANGO_SECRET_KEY`, `DEBUG`, or SMTP settings. Compose interpolates these into the container via the `environment:` section, and sensible defaults apply when no `.env` file is present — so the default `docker compose up --build` works out of the box.

The compose setup creates two named volumes so your data persists across rebuilds:
- `lms_data` — SQLite database file (`/data/db.sqlite3` inside the container)
- `lms_media` — Uploaded images (`/app/lms_project/media` inside the container)

On first startup the container seeds the volume with the project's existing `lms_project/db.sqlite3` (sample data, demo accounts, etc.) so the dockerized app starts populated. On subsequent runs the volume's existing DB is preserved and never overwritten.

Supported environment variables (all optional, sensible defaults applied):

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (set a long random value for production) |
| `DEBUG` | `True` / `False` |
| `DATABASE_PATH` | SQLite file path inside the container |
| `EMAIL_BACKEND` | Django email backend |
| `EMAIL_HOST`, `EMAIL_PORT` | SMTP host and port |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials (leave blank to fall back to console email backend) |
| `DEFAULT_FROM_EMAIL` | "From" address for outgoing mail |

The container runs migrations on startup and serves the app via gunicorn on port 5000.

### Bootstrap an initial admin (one-shot)

To get a usable admin account on the very first `docker compose up --build`, set the following in your `.env` (or shell environment) before bringing the stack up:

```env
INITIAL_ADMIN_EMAIL=admin@example.com
INITIAL_ADMIN_PASSWORD=change-me-on-first-login
INITIAL_ADMIN_NAME=Initial Admin   # optional, defaults to "Initial Admin"
```

On every container start, after migrations run, the `bootstrap_admin` management command checks for an `Admin` with that email:
- If neither variable is set, the step is skipped silently.
- If no admin with that email exists, a new **superadmin** record is created with the given password.
- If an admin with that email already exists, the record is left **untouched** — the password is **never** overwritten on subsequent runs. Change the password from inside the admin portal.

This makes `docker compose up --build` a true one-command setup: bring up the stack, then log into the admin portal with the credentials you configured.

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
