#Authentication helper functions.

from sqlalchemy.orm import Session
from database.models import User
from core.security import verify_password
from fastapi import HTTPException , status

def authenticate_user(db: Session, email: str, password: str):
    user=db.query(User).filter(User.email==email).first()
    if not user : 
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    if not verify_password(password , user.hashed_password):
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password")
    
    return user

def get_current_user():
    pass
