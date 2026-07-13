#!/bin/sh
set -e

echo "==> Waiting for MySQL (voluntarios)..."
while ! python3 -c "import socket; s=socket.socket(); s.connect(('mysql-voluntarios', 3306)); s.close()" 2>/dev/null; do
  sleep 1
done
echo "==> MySQL is ready!"

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Creating system user for BFF..."
python manage.py shell -c "
from django.contrib.auth.models import User
User.objects.get_or_create(id=1, defaults={'username': 'bff-system', 'is_active': True})
" 2>/dev/null || true

echo "==> Starting server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:8005 --workers 1 --threads 2 --timeout 120
