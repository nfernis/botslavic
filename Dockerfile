FROM python:3.10-slim-buster

WORKDIR /app

ENV PORT=80

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT gunicorn --bind 0.0.0.0:$PORT app:app
