#!/bin/sh

echo "Running migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting server..."
if [ "$DEBUG" = "True" ] || [ "$DEBUG" = "true" ]; then
    python manage.py runserver 0.0.0.0:8000
else
    gunicorn todoapi.wsgi:application --bind 0.0.0.0:8000
fi
