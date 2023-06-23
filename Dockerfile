FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --upgrade pip && pip install -r /app/requirements.txt --no-cache-dir && apt-get install -y locales && locale-gen ru_RU.UTF-8 && export LC_ALL=ru_RU.UTF-8 && export LANG=ru_RU.UTF-8

CMD ["gunicorn", "config.wsgi:application", "--bind", "0:8000" ] 