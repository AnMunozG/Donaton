#!/bin/sh
set -e

echo "==> Waiting for MySQL (usuarios)..."
while ! python3 -c "import socket; s=socket.socket(); s.connect(('mysql-usuarios', 3306)); s.close()" 2>/dev/null; do
  sleep 1
done
echo "==> MySQL is ready!"

echo "==> Running migrations..."
python manage.py migrate --noinput

echo "==> Running seed..."
python manage.py seed

echo "==> Starting server..."
exec python manage.py runserver 0.0.0.0:8000
