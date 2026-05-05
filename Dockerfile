FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libjpeg-dev \
        zlib1g-dev \
        libfreetype6-dev \
        liblcms2-dev \
        libwebp-dev \
        libtiff-dev \
        libopenjp2-7-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml ./
RUN pip install \
        "django>=5.2.8" \
        "gunicorn>=23.0.0" \
        "pillow>=12.1.0" \
        "reportlab>=4.0.0"

COPY . .

WORKDIR /app/lms_project

RUN python manage.py collectstatic --noinput || true

RUN mkdir -p /data /app/lms_project/media

EXPOSE 5000

CMD ["sh", "-c", "python manage.py migrate --noinput && gunicorn --bind 0.0.0.0:5000 --workers 3 --access-logfile - --error-logfile - lms_project.wsgi:application"]
