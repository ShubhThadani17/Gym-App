#Defines database tables.

from sqlalchemy import Column , Integer , String , Date , ForeignKey
from sqlalchemy.orm import declarative_base, relationship 

Base=declarative_base()

class User(Base):
    __tablename__ = "users"

    id=Column(Integer , primary_key=True , index=True)
    username=Column(String , unique=True , index=True)
    email=Column(String , unique=True , index=True)
    hashed_password=Column(String)
    members = relationship("Member", back_populates="user")

class Member(Base):
    __tablename__ = "members"

    id=Column(Integer , primary_key=True , index=True)
    name=Column(String , index=True)
    email=Column(String , unique=True , index=True)
    phone=Column(String , unique=True , index=True)
    age=Column(Integer)
    gender=Column(String)
    created_at=Column(Date)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="members")