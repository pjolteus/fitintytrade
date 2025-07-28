
# FitintyTrade Alerting Setup (Optional)

## Option 1: Slack/Discord Webhook

1. Create a webhook URL
2. Add this to `.env`:
   ALERT_WEBHOOK_URL=https://your-webhook-url

3. Use this in Python:
```python
import requests, os

def send_alert(msg):
    url = os.getenv("ALERT_WEBHOOK_URL")
    if url:
        requests.post(url, json={"content": msg})
```

## Option 2: Email Alerts

- Use `smtplib` or a tool like SendGrid or Mailgun
