#!/bin/sh
set -e

# Wait for the MySQL port to be available
until nc -z "mysql" 3306; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - running migrations"
python binaryblade24/manage.py migrate