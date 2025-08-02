# -------- Stage 1: Build Frontend --------
FROM node:18-alpine AS frontend

WORKDIR /app
COPY frontend_ui/ ./
RUN npm install && npm run build


# -------- Stage 2: Backend and Broker --------
FROM python:3.10-slim AS backend

WORKDIR /app

# System deps
RUN apt-get update && apt-get install -y git && apt-get clean

# Install Python deps
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY backend_api /app/backend_api
COPY broker_execution /app/broker_execution

# Optional: serve frontend via FastAPI static route
COPY --from=frontend /app/dist /app/backend_api/static

ENV PYTHONPATH=/app/backend_api:/app/broker_execution

# Run backend
CMD ["uvicorn", "backend_api.main:app", "--host", "0.0.0.0", "--port", "8000"]
