#!/usr/bin/env bash
# start-server.sh
echo "Hello from IAD"
uv run manage.py collectstatic --no-input
if [ -n "$MIGRATE" ] ; then
    (echo "making migrations and running them"
    uv run manage.py makemigrations --no-input
    uv run manage.py migrate --no-input)
fi
if [ -n "$DJANGO_SUPERUSER_USERNAME" ] && [ -n "$DJANGO_SUPERUSER_PASSWORD" ] ; then
    (echo "creating superuser ${DJANGO_SUPERUSER_USERNAME}" && uv run manage.py createsuperuser --no-input --noinput --email 'blank@email.com')
fi
uv run gunicorn iad.wsgi --user www-data --bind 0.0.0.0:8010 --timeout 360 --workers 3 & nginx -g "daemon off;"