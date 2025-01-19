#!/usr/bin/env bash

set -o errexit
set -o nounset
set -o pipefail

readonly cmd="$*"

echo "Django environment is $DJANGO_ENV."

if [ "$cmd" = "start_app" ]; then
  cd source
  python manage.py migrate --noinput
  python manage.py loaddata fixtures/sensors.json fixtures/sensor_readings.json

  if [ "$DJANGO_ENV" = "dev" ]; then
    python -Wd manage.py runserver 0.0.0.0:8000
  else
     gunicorn base.wsgi:application --config gunicorn.conf.py
  fi
else
  # shellcheck disable=SC2086
  exec $cmd
fi
