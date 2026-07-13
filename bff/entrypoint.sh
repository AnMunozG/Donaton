#!/bin/sh
set -e

echo "==> Running BFF migrations..."
python manage.py migrate --noinput

echo "==> Starting BFF server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8080 --workers 1 --threads 2 --timeout 120
