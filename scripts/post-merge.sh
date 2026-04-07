#!/bin/bash
set -e

cd lms_project
python manage.py migrate --no-input
