#!/bin/sh
set -e

DB_PATH="${DATABASE_PATH:-/data/db.sqlite3}"
SEED_DB="/app/seed/db.sqlite3"

mkdir -p "$(dirname "$DB_PATH")"

if [ ! -f "$DB_PATH" ] && [ -f "$SEED_DB" ]; then
    echo "Seeding database from $SEED_DB -> $DB_PATH"
    cp "$SEED_DB" "$DB_PATH"
fi

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn on 0.0.0.0:5000"
exec gunicorn \
    --bind 0.0.0.0:5000 \
    --workers 3 \
    --access-logfile - \
    --error-logfile - \
    lms_project.wsgi:application
