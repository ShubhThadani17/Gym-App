#Business logic for members.

from sqlalchemy.orm import Session
from database.models import Member
from fastapi import HTTPException , status

def create_member(db : Session , member_data):
    new_member = Member(**member_data)
    db.add(new_member)
    db.commit()
    db.refresh(new_member)
    return {"message":"Member created successfully" , "member":new_member.name}


def get_member(db :Session , member_id : int):
    return db.query(Member).filter(Member.id == member_id).first()


def get_all_members(db : Session):
    return db.query(Member).all()


def update_member(db:Session , member_id:int , new_data):
    member = db.query(Member).filter(Member.id==member_id).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    
    for key , value in new_data.items():
        setattr(member , key , value)
    db.commit()
    db.refresh(member)
    return member


def delete_member(db:Session , member_id:int):
    member = db.query(Member).filter(Member.id==member_id).first()
    if not member :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Member not found")
    db.delete(member)
    db.commit()
