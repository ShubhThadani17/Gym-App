#Defines API request/response structures.

from pydantic import BaseModel
from datetime import date
from typing import Optional

class UserRegister(BaseModel):

    email:str
    password:str

class MemberCreate(BaseModel):
    name:str
    email:str
    phone:str
    age:int
    gender:str

class MemberUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    age: Optional[int] = None
    gender: Optional[str] = None

class SubscriptionCreate(BaseModel):
    member_id:int
    start_date:date
    end_date:date
    status:str

class SubscriptionUpdate(BaseModel):
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    status:Optional[str] = None

class PaymentCreate(BaseModel):
    member_id:int 
    amount : float
    payment_method : str
    status: str = "pending"

class DashboardResponse(BaseModel):
    total_members: int
    active_subscriptions: int
    expired_subscriptions: int
    total_revenue: float