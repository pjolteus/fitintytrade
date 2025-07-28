from fastapi import FastAPI
from .app.api import routes
from .app.routes import user
from deploy.monitoring.logging_config import setup_logging
from deploy.monitoring.health import router as health_router
from deploy.monitoring.metrics import router as metrics_router

setup_logging("backend")
app = FastAPI()
app.include_router(routes.router)
app.include_router(health_router)
app.include_router(metrics_router)
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.trustedhost import TrustedHostMiddleware
from starlette.responses import JSONResponse

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware

from dependencies.auth import get_current_user
from .app.schemas import auth
from .schemas.auth import User
from routes import user  # adjust import if your structure differs

from backend.routes import email_report

import logging
import time
import redis
import psycopg2
from db.connection import engine, Base
from api.routes import api_router
from config import settings

# --------------------------------
# 🚀 Validate Critical Environment
# --------------------------------
logging.info(f"🚀 Starting FitintyTrade in {settings.MODE} mode")

if not settings.JWT_SECRET_KEY:
    raise RuntimeError("Missing JWT_SECRET_KEY in environment")

app = FastAPI()

app.include_router(user.router, prefix="/api/user", tags=["User"])
# ------------------------
# Initialize FastAPI App
# ------------------------
app = FastAPI(
    title="FitintyTrade AI API",
    description="AI-powered options prediction engine for daily stock/currency/crypto trades",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# ------------------------
# CORS Configuration (from .env)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# Logging Middleware
# ------------------------
class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        duration = time.time() - start_time
        logging.info(
            f"{request.method} {request.url.path} - {response.status_code} - {duration:.4f}s"
        )
        return response

app.add_middleware(LoggingMiddleware)

# ------------------------
# Trusted Hosts
# ------------------------
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["fitinty.com", "*.fitinty.com", "localhost", "127.0.0.1"]
)

# ------------------------
# Rate Limiting
# ------------------------
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(429, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

# ------------------------
# Global Exception Handling
# ------------------------
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logging.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error. Please try again later."}
    )

# ------------------------
# Startup & Shutdown Events
# ------------------------
@app.on_event("startup")
async def on_startup():
    logging.info("✅ FastAPI startup event triggered")

    # Test PostgreSQL connection
    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.close()
        logging.info("✅ PostgreSQL connection OK")
    except Exception as db_error:
        logging.error(f"❌ PostgreSQL connection failed: {db_error}")
        raise

    # Test Redis connection
    try:
        redis_client = redis.Redis.from_url(settings.REDIS_URL)
        redis_client.ping()
        logging.info("✅ Redis connection OK")
    except Exception as redis_error:
        logging.error(f"❌ Redis connection failed: {redis_error}")
        raise

    Base.metadata.create_all(bind=engine)

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("🛑 Shutting down FitintyTrade API...")

# ------------------------
# Health Check Endpoint
# ------------------------
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

# ------------------------
# Debug Env Viewer (DEV only)
# ------------------------
@app.get("/env/debug", tags=["Admin"])
async def debug_env(user: User = Depends(get_current_user)):
    if settings.MODE != "DEV":
        return JSONResponse(status_code=403, content={"detail": "Access denied"})
    return {
        "MODE": settings.MODE,
        "USER": user.email,
        "IS_TESTING": settings.IS_TESTING,
        "DATABASE_URL": settings.DATABASE_URL,
        "REDIS_URL": settings.REDIS_URL,
        "LSTM_MODEL_PATH": settings.LSTM_MODEL_PATH,
        "CELERY_BROKER_URL": settings.CELERY_BROKER_URL,
        "CELERY_RESULT_BACKEND": settings.CELERY_RESULT_BACKEND
    }

# ------------------------
# Mount API Routes
# ------------------------
app.include_router(api_router, prefix="/api")
app.include_router(email_report.router, prefix="/api")