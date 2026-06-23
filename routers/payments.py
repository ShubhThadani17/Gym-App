
from fastapi import APIRouter , Depends
from services.payment_service import create_payment , get_payment , get_all_payments , get_member_payments , total_revenue
from database.db import get_db
from core.auth import get_current_user
from database.models import User 
from database.schemas import PaymentCreate , PaymentResponse
from typing import List

router=APIRouter()

@router.post("/payments", response_model=PaymentResponse)
def create_payment_endpoint(payment_data : PaymentCreate , db = Depends(get_db) , current_user : User = Depends(get_current_user)):
    return create_payment(db=db , payment_data=payment_data, user_id=current_user.id)

@router.get("/payments/total-revenue")
def get_total_revenue(db = Depends(get_db) ,current_user : User = Depends(get_current_user)):
    return total_revenue(db=db,user_id=current_user.id)

@router.get("/payments/{payment_id}", response_model=PaymentResponse)
def get_payment_endpoint(payment_id : int , db = Depends(get_db) ,current_user : User = Depends(get_current_user)):
    return get_payment(db=db , payment_id=payment_id,user_id=current_user.id)

@router.get("/payments", response_model=List[PaymentResponse])
def get_all_payment_endpoint(db = Depends(get_db) ,current_user : User = Depends(get_current_user)):
    return get_all_payments(db=db,user_id=current_user.id)

@router.get("/payments/member/{member_id}", response_model=List[PaymentResponse])
def get_member_payments_endpoint(member_id : int , db = Depends(get_db) ,current_user : User = Depends(get_current_user)):
    return get_member_payments(db=db,member_id=member_id , user_id=current_user.id)