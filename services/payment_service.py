
from sqlalchemy.orm import Session
from database.models import Payment , Member
from fastapi import HTTPException , status
from sqlalchemy import func

def create_payment(db : Session , payment_data,user_id: int):
    member = (db.query(Member).filter(Member.id == payment_data.member_id,Member.user_id == user_id).first())

    if not member:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Member not found")
    new_payment = Payment(**payment_data.model_dump())
    db.add(new_payment)
    db.commit()
    db.refresh(new_payment)
    return new_payment

def get_payment(db : Session , payment_id : int,user_id: int):
    payment = (db.query(Payment).join(Member).filter(Payment.id == payment_id,Member.user_id == user_id).first())

    if not payment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")

    return payment


def get_all_payments(db : Session , user_id :int ):
    return (db.query(Payment).join(Member).filter(Member.user_id == user_id).all())


def get_member_payments(db : Session , member_id: int ,user_id: int):
    payments = (db.query(Payment).join(Member).filter(Payment.member_id == member_id,Member.user_id == user_id).all())
    if not payments:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Payment not found")
    return payments

def total_revenue(db : Session,user_id: int):
    result = (db.query(func.sum(Payment.amount)).join(Member).filter(Member.user_id == user_id).scalar())

    return {"total_revenue": result or 0}