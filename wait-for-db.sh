#!/bin/sh
# wait-for-db.sh

# This script waits for a PostgreSQL database to be available.
# It parses the host and port from the DATABASE_URL environment variable.

set -e

# The command to run after the database is up
cmd="$@"

# If DATABASE_URL is not set, exit with an error
if [ -z "$DATABASE_URL" ]; then
  >&2 echo "Error: DATABASE_URL is not set."
  exit 1
fi

# Extract host and port from DATABASE_URL (e.g., postgres://user:pass@host:port/db)
# This uses basic shell tools to be lightweight.
DB_HOST=$(echo "$DATABASE_URL" | sed -e 's,.*@,,' -e 's,:.*,,' -e 's,/.*,,')
DB_PORT=$(echo "$DATABASE_URL" | sed -e 's,.*:,,' -e 's,/.*,,')

# Wait for the database port to be available
while ! nc -z "$DB_HOST" "$DB_PORT"; do
  >&2 echo "PostgreSQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "PostgreSQL is up - executing command"
exec $cmd