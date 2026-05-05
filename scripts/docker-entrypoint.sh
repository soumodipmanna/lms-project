#!/bin/sh
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Bootstrapping initial admin (if configured)..."
python manage.py bootstrap_admin

echo "Seeding demo users..."
python manage.py seed_demo_users

echo "Seeding books..."
python manage.py seed_books

echo "Starting gunicorn on 0.0.0.0:5000"
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    lms_project.wsgi:application
