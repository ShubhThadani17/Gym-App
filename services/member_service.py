#Business logic for members.

from sqlalchemy.orm import Session
from database.models import Member
from fastapi import HTTPException , status
from sqlalchemy import func

def create_member(db : Session , member_data, user_id : int):
    new_member = Member(**member_data.model_dump(),user_id=user_id)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return new_member


def get_member(db :Session , member_id : int , user_id: int):
    return db.query(Member).filter(Member.id == member_id, Member.user_id == user_id).first()


def get_all_members(db : Session, user_id:int):
     return (db.query(Member).filter(Member.user_id == user_id).all())

def search_member(db : Session, user_id:int , name : str):
    return (db.query(Member).filter(Member.user_id == user_id,func.lower(Member.name).contains(name.lower())).all())


def update_member(db:Session , member_id:int , new_data , user_id:int):
    member = db.query(Member).filter(Member.id==member_id, Member.user_id == user_id).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    for key , value in new_data.items():
        setattr(member , key , value)
    db.commit()
    db.refresh(member)
    return member


def delete_member(db:Session , member_id:int , user_id:int):
    member = db.query(Member).filter(Member.id==member_id,Member.user_id == user_id).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    db.delete(member)
    db.commit()
    return {"message": "Member deleted successfully"}