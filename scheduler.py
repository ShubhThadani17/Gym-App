

from apscheduler.schedulers.background import BackgroundScheduler

from database.db import SessionLocal
from services.email_service import send_expiry_email
from services.reminder_service import get_expiring_subscriptions
from services.subscription_service import expire_subscriptions


def send_subscription_reminders():

    db = SessionLocal()

    try:
        subscriptions = get_expiring_subscriptions(db)

        for subscription in subscriptions:

            member = subscription.member

            send_expiry_email(
                member.email,
                member.name
            )

    finally:
        db.close()

def auto_expire_subscriptions():

    db = SessionLocal()

    try:
        expire_subscriptions(db)

    finally:
        db.close()


scheduler = BackgroundScheduler()

scheduler.add_job(
    send_subscription_reminders,
    "cron",
    hour=9,
    minute=0
)

scheduler.add_job(
    auto_expire_subscriptions,
    "cron",
    hour=0,
    minute=0
)