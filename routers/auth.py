#API endpoints

from fastapi import FastAPI , Depends , HTTPException , status
from core.security import hash_password , verify_password , create_access_token
from database.schemas import UserCreate, UserRegister
from core.auth import authenticate_user
from database.db import get_db

app=FastAPI()

@app.post("/register")
def register(user: UserRegister , db=Depends(get_db)):
    client= db.query(UserCreate).filter(UserCreate.email==user.email).first()
    if client:
        return HTTPException(status_code=400 , detail = "Email Already Exists")
    hashed_password=hash_password(user.password)
    new_user = UserCreate(email=user.email , hashed_password=hashed_password)
    db.add(new_user)
    db.commit()

    return {"message":"User registered , Please Login"}

@app.post("/login")
def login(user: UserRegister , db=Depends(get_db)):
    db_user=authenticate_user(db , user.email , user.password)
    if not db_user:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED , detail="Invalid Credentials")
    
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token , "token_type":"bearer"}