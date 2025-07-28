# backend/utils/email_utils.py
from email.message import EmailMessage
import aiosmtplib
from jinja2 import Template

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USERNAME = "your-email@gmail.com"
SMTP_PASSWORD = "your-app-password"

def format_html(predictions):
    rows = "".join(
        f"<tr><td>{p.ticker}</td><td>{'Call' if p.prediction else 'Put'}</td><td>{p.confidence:.2f}</td><td>{p.model_name}</td><td>{p.timestamp.strftime('%Y-%m-%d %H:%M')}</td></tr>"
        for p in predictions
    )
    return f"""
    <h2>Selected Prediction Report</h2>
    <table border="1" cellpadding="5" cellspacing="0">
        <tr><th>Ticker</th><th>Prediction</th><th>Confidence</th><th>Model</th><th>Timestamp</th></tr>
        {rows}
    </table>
    """

async def send_prediction_report_email(predictions, to_email):
    msg = EmailMessage()
    msg["Subject"] = "Prediction Report"
    msg["From"] = SMTP_USERNAME
    msg["To"] = to_email
    msg.set_content("Your prediction report is attached in HTML format.", subtype="plain")
    msg.add_alternative(format_html(predictions), subtype="html")

    await aiosmtplib.send(
        msg,
        hostname=SMTP_HOST,
        port=SMTP_PORT,
        start_tls=True,
        username=SMTP_USERNAME,
        password=SMTP_PASSWORD,
    )
