#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python binaryblade24/manage.py collectstatic --no-input
python binaryblade24/manage.py migrate

# Create superuser
python binaryblade24/manage.py createsuperuser --no-input --username admin --email admin@example.com