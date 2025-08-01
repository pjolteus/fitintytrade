# Backend Dockerfile for FitintyTrade
FROM python:3.10-slim

WORKDIR /app

# Copy requirements early for better layer caching
COPY backend_api/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy both backend_api and broker_execution folders
COPY backend_api /app/backend_api
COPY broker_execution /app/broker_execution

# Set PYTHONPATH to include both modules
ENV PYTHONPATH=/app/backend_api:/app/broker_execution

# Run the FastAPI app
CMD ["uvicorn", "backend_api.main:app", "--host", "0.0.0.0", "--port", "8000"]

