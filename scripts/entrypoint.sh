#!/bin/sh
#
# Performs setup operations for the project in production mode.

python manage.py migrate --no-input
python manage.py check --deploy --settings config.settings

gunicorn config.wsgi:application --bind 0.0.0.0:"$APP_PORT" --access-logfile -