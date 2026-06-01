#!/bin/sh

echo "Applying migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn atlas.wsgi:application --bind 0.0.0.0:8001