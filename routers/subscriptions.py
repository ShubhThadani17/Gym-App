#subscription endpoints

from fastapi import APIRouter , Depends , HTTPException , status
from services.subscription_service import create_subscription , get_subscription , get_all_subscriptions , renew_subscription , cancel_subscription
from database.db import get_db
from core.auth import get_current_user
from database.models import User

router=APIRouter()

@router.post("/subscriptions")
def create_subscription_endpoint(subscription_data : dict ,db =Depends(get_db) , current_user :User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    return create_subscription(db=db, subscription_data=subscription_data)

@router.get("/subscriptions/{subscription_id}")
def get_subsciption_endpoint(subscription_id : int ,db =Depends(get_db) , current_user :User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return get_subscription(db=db , subscription_id=subscription_id)

@router.get("/subscriptions")
def get_all_subscription_endpoint(db = Depends(get_db) , current_user :User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return get_all_subscriptions(db=db)

@router.put("/subscriptions/{subscription_id}/renew")
def renew_subscription_endpoint(subscription_id : int , new_data : dict , db= Depends(get_db) , current_user :User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return renew_subscription(db=db , subscription_id = subscription_id , new_data=new_data)

@router.delete("/subscriptions/{subscription_id}")
def delete_subscription_endpoint(subscription_id : int , new_data : dict , db= Depends(get_db) , current_user :User = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return cancel_subscription(db=db , subscription_id = subscription_id)
