#Defines API request/response structures.

from pydantic import BaseModel

class UserRegister(BaseModel):

    email:str
    password:str

class MemberCreate(BaseModel):
    name:str
    email:str
    phone:str
    age:int
    gender:str