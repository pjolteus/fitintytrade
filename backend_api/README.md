# Backend API - FitintyTrade

This is the FastAPI-based backend API layer for handling:
- Prediction requests
- Signal generation
- Celery background tasks
- Trade execution endpoints

### Structure
- `app/api`: API routes
- `app/services`: Core logic
- `app/db`: SQLAlchemy models and engine
- `app/tasks`: Celery workers
