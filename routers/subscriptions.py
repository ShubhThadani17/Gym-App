#subscription endpoints

from fastapi import APIRouter , Depends 
from services.subscription_service import create_subscription , get_subscription , get_all_subscriptions , renew_subscription , cancel_subscription
from database.db import get_db
from core.auth import get_current_user
from database.models import User
from database.schemas import SubscriptionCreate , SubscriptionUpdate , SubscriptionResponse
from typing import List

router=APIRouter()

@router.post("/subscriptions", response_model=SubscriptionResponse)
def create_subscription_endpoint(subscription_data : SubscriptionCreate ,db =Depends(get_db) , current_user :User = Depends(get_current_user)):
    return create_subscription(db, subscription_data,current_user.id)

@router.get("/subscriptions/{subscription_id}", response_model=SubscriptionResponse)
def get_subsciption_endpoint(subscription_id : int ,db =Depends(get_db) , current_user :User = Depends(get_current_user)):
    return get_subscription(db , subscription_id,current_user.id)

@router.get("/subscriptions", response_model=List[SubscriptionResponse])
def get_all_subscription_endpoint(db = Depends(get_db) , current_user :User = Depends(get_current_user)):
    return get_all_subscriptions(db , current_user.id)

@router.post("/subscriptions/{subscription_id}/renew", response_model=SubscriptionResponse)
def renew_subscription_endpoint(subscription_id : int , db= Depends(get_db) , current_user :User = Depends(get_current_user)):
    return renew_subscription(db , subscription_id ,current_user.id)

@router.delete("/subscriptions/{subscription_id}")
def delete_subscription_endpoint(subscription_id : int  , db= Depends(get_db) , current_user :User = Depends(get_current_user)):  
    return cancel_subscription(db , subscription_id,current_user.id)