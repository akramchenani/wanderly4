#!/usr/bin/env bash
# Render runs this script every time you deploy.
set -o errexit   # exit on first error

pip install -r requirements.txt

# Collect static files into /staticfiles
python manage.py collectstatic --no-input

# Apply any pending database migrations
python manage.py migrate
