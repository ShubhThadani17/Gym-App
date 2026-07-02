
from datetime import date, timedelta
from database.models import Subscription, Member


def get_expiring_subscriptions(db):

    tomorrow = date.today() + timedelta(days=1)

    return (db.query(Subscription).join(Member).filter(Subscription.end_date == tomorrow).all())

