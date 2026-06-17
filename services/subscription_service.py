#Keeps subscription logic

from sqlalchemy.orm import Session
from database.models import Subscription
from fastapi import HTTPException , status

def create_subscription(db:Session , subscription_data):
    new_subscription = Subscription(**subscription_data)
    db.add(new_subscription)
    db.commit()
    db.refresh(new_subscription)
    return new_subscription

def get_subscription(db:Session , subscription_id:int):
    return db.query(Subscription).filter(Subscription.id==subscription_id).first()

def get_all_subscriptions(db:Session):
    return db.query(Subscription).all()

def renew_subscription(db:Session , subscription_id:int , new_data):
    subscription = db.query(Subscription).filter(Subscription.id==subscription_id).first()
    if not subscription :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    
    for key , value in new_data.items():
        setattr(subscription , key , value)
    db.commit()
    db.refresh(subscription)
    return subscription

def cancel_subscription(db:Session , subscription_id:int):
    subscription = db.query(Subscription).filter(Subscription.id==subscription_id).first()
    if not subscription : 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Subscription not found")
    db.delete(subscription)
    db.commit()
    return {"message":"Subscription deleted successfully"}