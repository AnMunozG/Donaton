#!/bin/sh
set -e

echo "==> Running BFF migrations..."
python manage.py migrate --noinput

echo "==> Starting BFF server..."
exec python manage.py runserver 0.0.0.0:8080
