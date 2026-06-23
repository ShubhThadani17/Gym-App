
import smtplib
import logging
from email.message import EmailMessage
from core.config import settings

logger = logging.getLogger(__name__)

def send_expiry_email(to_email: str, member_name: str):

    msg = EmailMessage()
    msg["Subject"] = "Gym Subscription Expiring Tomorrow"
    msg["From"] = settings.EMAIL_ADDRESS
    msg["To"] = to_email

    msg.set_content(
        f"""
Hello {member_name},

Your gym subscription will expire tomorrow.

Please renew your subscription to continue enjoying gym access.

Thank You.
"""
    )
    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(settings.EMAIL_ADDRESS, settings.EMAIL_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")