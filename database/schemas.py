#Defines API request/response structures.

from pydantic import BaseModel

class UserRegister(BaseModel):

    email:str
    password:str