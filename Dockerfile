# Use a lightweight official Python image
FROM python:3.11-alpine

# Set the working directory
WORKDIR /app

# Copy requirements before installing them (leverages Docker caching)
COPY requirements.txt /app/

# Install build dependencies, install requirements, and clean up to keep the image small
# netcat-openbsd is for your wait-for-db.sh script
RUN apk add --no-cache netcat-openbsd \
    && apk add --no-cache --virtual .build-deps mariadb-dev gcc musl-dev python3-dev \
    && pip install -r requirements.txt \
    && apk del .build-deps

# Copy the rest of the application code (ensure .dockerignore is used)
COPY . /app/

# Copy and make the waiter script executable
COPY wait-for-db.sh /app/
RUN chmod +x /app/wait-for-db.sh

# Collect static files with a dummy secret key and correct path
RUN SECRET_KEY=dummy-for-build-only python binaryblade24/manage.py collectstatic --noinput

# Expose the port the app runs on
EXPOSE 8000

# Start the application using the waiter script
# Corrected the path to the wsgi application
CMD ["/app/wait-for-db.sh", "gunicorn", "binaryblade24.binaryblade24.wsgi", "--bind", "0.0.0.0:8000"]
