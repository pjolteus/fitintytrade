# 🌐 FitintyTrade Environment Variables

This document explains the purpose of each environment variable used in the platform. Do **not** share your `.env` file publicly.

---

## 🔧 Application Core

| Key | Description |
|-----|-------------|
| `MODE` | App mode (`DEV`, `PROD`, `DOCKER`, `RAILWAY`) |
| `IS_TESTING` | Enable test mode for CI/CD |

---

## 🗄 Database

| Key | Description |
|-----|-------------|
| `DATABASE_URL` | Full PostgreSQL connection string |

---

## 🔐 JWT Authentication

| Key | Description |
|-----|-------------|
| `JWT_SECRET_KEY` | Secret for signing JWTs |
| `JWT_ALGORITHM` | Algorithm (usually HS256) |
| `JWT_EXPIRE_MINUTES` | Token expiration in minutes |

---

## 🌍 CORS

| Key | Description |
|-----|-------------|
| `BACKEND_CORS_ORIGINS` | Allowed frontend origins (comma-separated URLs) |

---

## 🔁 Celery & Redis

| Key | Description |
|-----|-------------|
| `REDIS_URL` | Redis base URL |
| `CELERY_BROKER_URL` | Redis queue for Celery |
| `CELERY_RESULT_BACKEND` | Redis DB for task results |

---

## 🧠 AI Models

| Key | Description |
|-----|-------------|
| `LSTM_MODEL_PATH` | Path to saved PyTorch model file |

---

## 📧 Email Alerts (Optional)

| Key | Description |
|-----|-------------|
| `SMTP_SERVER` | SMTP server host |
| `SMTP_PORT` | SMTP port |
| `EMAIL_FROM` | Sender email |
| `EMAIL_PASSWORD` | SMTP auth password |
| `ALERT_EMAIL` | From address for system alerts |
| `DEV_EMAIL` | To address for receiving errors |

---

## 🤖 Broker API Keys (Optional)

| Key | Description |
|-----|-------------|
| `ALPACA_API_KEY`, `ALPACA_SECRET_KEY` | Alpaca trading keys |
| `OANDA_API_KEY`, `OANDA_ACCOUNT_ID` | OANDA keys |
| `FXCM_API_TOKEN`, `FXCM_ACCOUNT_ID` | FXCM account access |
| `IBR_USERNAME`, `IBR_PASSWORD`, `IBR_ACCOUNT_ID` | Interactive Brokers login |
| `BINANCE_API_KEY`, `BINANCE_SECRET_KEY` | Binance Spot account keys |

---

## 💡 Tips

- Keep your `.env` out of version control (`.gitignore`)
- Use `.env.example` as a safe template for other developers
- Use `config/env_settings.py` to load env vars in all modules
