#Defines database tables.

from sqlalchemy import Column , Integer , String , Date , ForeignKey
from sqlalchemy.orm import declarative_base, relationship 
from datetime import date

Base=declarative_base()

class User(Base):
    __tablename__ = "users"

    id=Column(Integer , primary_key=True , index=True)
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
    created_at=Column(Date, default=date.today)

    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="members")
    subscription = relationship("Subscription",back_populates="member",uselist=False)
    payments = relationship("Payment",back_populates="member")

class Subscription(Base):
    __tablename__ = "subscriptions"

    id=Column(Integer , primary_key=True , index=True)
    member_id=Column(Integer , ForeignKey("members.id"))
    start_date=Column(Date)
    end_date=Column(Date)
    status=Column(String)

    member = relationship("Member", back_populates="subscription")

class Payment(Base):
    __tablename__ = "payments"

    id=Column(Integer , primary_key=True , index=True)
    member_id=Column(Integer , ForeignKey("members.id"))
    amount=Column(Integer)
    payment_date=Column(Date, default=date.today)
    payment_method=Column(String)
    status=Column(String)

    member = relationship("Member",back_populates="payments")