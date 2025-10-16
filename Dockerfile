FROM python:alpine

WORKDIR /app

COPY requirements.txt /app/

RUN apk add --no-cache netcat-openbsd mariadb-dev gcc musl-dev python3-dev
RUN pip install -r requirements.txt

COPY . /app/

COPY wait-for-db.sh /app/
RUN chmod +x /app/wait-for-db.sh

RUN python binaryblade24/manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "binaryblade24.wsgi:application", "--bind", "0.0.0.0:8000"]
