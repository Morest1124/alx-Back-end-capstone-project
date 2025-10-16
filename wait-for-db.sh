#!/bin/sh
# wait-for-db.sh

set -e

host="$1"
shift
cmd="$@"

# Wait for the MySQL port to be available
until nc -z "$host" 3306; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd
