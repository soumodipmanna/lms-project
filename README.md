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

The compose setup starts two services:
- `db` — PostgreSQL 16 (production-grade storage with safe concurrent writes)
- `web` — Django app served by gunicorn on port 5000

And two named volumes so your data persists across rebuilds:
- `lms_pgdata` — PostgreSQL data directory
- `lms_media` — Uploaded images (`/app/lms_project/media` inside the container)

The web container waits for Postgres to become healthy, runs migrations on startup, then serves the app via gunicorn on port 5000.

Supported environment variables (all optional, sensible defaults applied):

| Variable | Purpose |
| --- | --- |
| `DJANGO_SECRET_KEY` | Django secret key (set a long random value for production) |
| `DEBUG` | `True` / `False` |
| `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_HOST`, `POSTGRES_PORT` | Postgres connection (used by the bundled `db` service) |
| `DATABASE_URL` | Single connection string (e.g. `postgres://user:pass@host:5432/db`); takes precedence over the discrete `POSTGRES_*` vars |
| `DATABASE_PATH` | SQLite file path inside the container — only used by the SQLite fallback when no Postgres vars are set |
| `EMAIL_BACKEND` | Django email backend |
| `EMAIL_HOST`, `EMAIL_PORT` | SMTP host and port |
| `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | SMTP credentials (leave blank to fall back to console email backend) |
| `DEFAULT_FROM_EMAIL` | "From" address for outgoing mail |

### Database configuration

The Django settings pick a database in this order:

1. `DATABASE_URL` (e.g. `postgres://user:pass@host:5432/dbname`) — takes precedence.
2. `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD` / `POSTGRES_HOST` / `POSTGRES_PORT` — used by the bundled compose stack (defaults: `lms` / `lms` / `lms` / `db` / `5432`).
3. SQLite fallback at `DATABASE_PATH` (or `BASE_DIR/db.sqlite3`) when none of the above are set — keeps `python manage.py runserver` working for local dev outside Docker with no extra setup.

When no Postgres vars are set, the container also seeds the SQLite volume on first startup with the project's existing `lms_project/db.sqlite3` (sample data, demo accounts) so a SQLite-only deployment starts populated. On subsequent runs the volume's existing DB is preserved and never overwritten. With Postgres in use, no SQLite seeding occurs.

### Migrating an existing SQLite database to Postgres

If you previously ran the SQLite-based compose stack and want to keep your data:

```bash
# 1. Start ONLY the old SQLite stack and dump its data (run from a checkout
#    that still uses SQLite, or temporarily unset the POSTGRES_* env vars):
docker compose run --rm web python manage.py dumpdata \
    --natural-foreign --natural-primary \
    -e contenttypes -e auth.Permission \
    --indent 2 > backup.json

# 2. Bring up the new Postgres-backed stack and load the dump:
docker compose up -d --build
docker compose exec web python manage.py loaddata /app/backup.json
```

Copy `backup.json` into the web container (e.g. via a bind mount or
`docker cp lms-web:/app/ backup.json`) before running `loaddata`.

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
