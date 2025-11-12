#!/bin/bash
# Production 

set -e # Stop the script if any command returns an error

python manage.py migrate --no-input
python manage.py collectstatic --no-input

# Run the main command (Dockerfile CMD)
exec "$@"