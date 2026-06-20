
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date

from database.models import Member, Subscription, Payment


def get_dashboard_stats(db: Session, user_id: int):

    total_members = (db.query(Member).filter(Member.user_id == user_id).count())

    active_subscriptions = (db.query(Subscription).join(Member).filter(Member.user_id == user_id, Subscription.status == "active").count())

    expired_subscriptions = (db.query(Subscription).join(Member).filter(Member.user_id == user_id, Subscription.status == "expired").count())

    total_revenue = (db.query(func.sum(Payment.amount)).join(Member).filter(Member.user_id == user_id).scalar()) or 0

    return {"total_members": total_members,"active_subscriptions": active_subscriptions,"expired_subscriptions": expired_subscriptions,"total_revenue": total_revenue}