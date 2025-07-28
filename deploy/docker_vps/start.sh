#!/bin/bash
echo "Starting FitintyTrade production environment..."
docker compose -f docker-compose.prod.yml up --build -d
