#!/bin/sh
set -e

echo "==> Waiting for MySQL (logistica)..."
while ! python3 -c "import socket; s=socket.socket(); s.connect(('mysql-logistica', 3306)); s.close()" 2>/dev/null; do
  sleep 1
done
echo "==> MySQL is ready!"

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Creating system user for BFF..."
python manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(id=1).exists():
    User.objects.create_user('bff_system', password=None, id=1)
    print('  -> System user created (id=1)')
else:
    print('  -> System user already exists')
"

echo "==> Starting server..."
exec python manage.py runserver 0.0.0.0:8001
