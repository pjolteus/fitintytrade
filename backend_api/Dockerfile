# -------- Stage 1: Build Frontend --------
FROM node:18-alpine AS frontend

WORKDIR /app
COPY frontend_ui/ ./
RUN npm install && npm run build


# -------- Stage 2: Backend + Broker + Supervisor --------
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y git supervisor && apt-get clean

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend and broker execution code
COPY backend_api /app/backend_api
COPY broker_execution /app/broker_execution

# Copy built frontend to backend static folder
COPY --from=frontend /app/dist /app/backend_api/static

# Copy supervisor config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

ENV PYTHONPATH=/app/backend_api:/app/broker_execution

EXPOSE 8000

CMD ["/usr/bin/supervisord", "-n"]

