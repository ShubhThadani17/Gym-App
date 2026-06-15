#API endpoints

from fastapi import APIRouter , Depends , HTTPException , status
from core.security import hash_password , verify_password , create_access_token
from database.schemas import UserRegister
from database.models import User
from core.auth import authenticate_user
from database.db import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserRegister , db=Depends(get_db)):
    client= db.query(User).filter(User.email==user.email).first()
    if client:
        raise HTTPException(status_code=400 , detail = "Email Already Exists")
    hashed_password=hash_password(user.password)
    new_user = User(email=user.email , hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message":"User registered , Please Login"}

@router.post("/login")
def login(user: UserRegister , db=Depends(get_db)):
    db_user=authenticate_user(db , user.email , user.password)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token , "token_type":"bearer"}