FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN apt-get update && pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ] 