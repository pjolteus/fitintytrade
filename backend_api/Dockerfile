# Backend Dockerfile for FitintyTrade
FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first for layer caching
COPY backend_api/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy backend and other folders into /app
COPY backend_api /app/backend_api
COPY broker_execution /app/broker_execution

# Set PYTHONPATH for both modules
ENV PYTHONPATH=/app/backend_api:/app/broker_execution

# Switch to backend working dir
WORKDIR /app/backend_api

# Run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
