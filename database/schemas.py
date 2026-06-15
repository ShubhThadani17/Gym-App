#Defines API request/response structures.

from pydantic import BaseModel

class UserCreate(BaseModel):

    username:str
    email:str
    password:str

class UserRegister(BaseModel):

    email:str
    password:str