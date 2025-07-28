
# Backend Dockerfile for FitintyTrade
FROM python:3.10-slim

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv celery redis

ENV PYTHONPATH=/app

CMD ["uvicorn", "backend_api.main:app", "--host", "0.0.0.0", "--port", "8000"]


