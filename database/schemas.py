#Defines API request/response structures.

from pydantic import BaseModel
from datetime import date
from typing import Optional , Literal , List

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
    status:Literal["active", "expired", "cancelled"] = "active"

class SubscriptionUpdate(BaseModel):
    start_date:Optional[date] = None
    end_date:Optional[date] = None
    status:Optional[str] = None

class PaymentCreate(BaseModel):
    member_id:int 
    amount : float
    payment_method : Literal["cash", "upi", "card", "online"]
    status: Literal["paid", "pending", "failed"] = "pending"

class DashboardResponse(BaseModel):
    total_members: int
    active_subscriptions: int
    expired_subscriptions: int
    total_revenue: float


class MemberResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: str
    age: int
    gender: str
    created_at: date

    model_config = {"from_attributes": True}


class SubscriptionResponse(BaseModel):
    id: int
    member_id: int
    start_date: date
    end_date: date
    status: str

    model_config = {"from_attributes": True}


class PaymentResponse(BaseModel):
    id: int
    member_id: int
    amount: float
    payment_date: date
    payment_method: str
    status: str

    model_config = {"from_attributes": True}


class UserResponse(BaseModel):
    id: int
    email: str

    model_config = {"from_attributes": True}
