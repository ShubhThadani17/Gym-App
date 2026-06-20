#Keeps subscription logic

from sqlalchemy.orm import Session
from database.models import Subscription , Member
from fastapi import HTTPException , status
from datetime import date , timedelta   

def create_subscription(db:Session , subscription_data , user_id:int):
    member = (db.query(Member).filter(Member.id == subscription_data.member_id,Member.user_id == user_id).first())
    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Member not found")
    new_subscription = Subscription(**subscription_data.model_dump())
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

def get_subscription(db:Session , subscription_id:int, user_id:int):
    subscription = (db.query(Subscription).join(Member).filter(Subscription.id == subscription_id,Member.user_id == user_id).first())
    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subscription not found")

    return subscription

def get_all_subscriptions(db:Session , user_id :int ):
    return (db.query(Subscription).join(Member).filter(Member.user_id == user_id).all())

def renew_subscription(db:Session , subscription_id:int ,user_id: int,new_data):
    subscription = (db.query(Subscription).join(Member).filter(Subscription.id == subscription_id,Member.user_id == user_id).first())

    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subscription not found")

    subscription.end_date = max(subscription.end_date, date.today()) + timedelta(days=30)
    subscription.status = "active"

    db.commit()
    db.refresh(subscription)
    return subscription

def cancel_subscription(db:Session , subscription_id:int,user_id: int):
    subscription = (db.query(Subscription).join(Member).filter(Subscription.id == subscription_id,Member.user_id == user_id).first())

    if not subscription:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Subscription not found")
    db.delete(subscription)
    db.commit()
    return {"message":"Subscription deleted successfully"}

def expire_subscriptions(db:Session):
    expired_subscriptions = (db.query(Subscription).filter(Subscription.end_date < date.today(),Subscription.status != "expired").all())

    for subscription in expired_subscriptions:
        subscription.status = "expired"

    db.commit()
    return len(expired_subscriptions)