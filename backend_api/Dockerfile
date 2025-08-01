# Backend Dockerfile for FitintyTrade
FROM python:3.10-slim

WORKDIR /app

# Copy only requirements first for layer caching
COPY backend_api/requirements.txt ./requirements.txt

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the full backend_api app
COPY backend_api /app

# Set PYTHONPATH so relative imports like `from app.schemas...` work
ENV PYTHONPATH=/app/backend_api:/app/broker_execution

# Expose the FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]





