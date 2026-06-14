#Authentication helper functions.
from passlib.context import CryptContext
from datetime import datetime, timedelta , timezone
from jose import jwt
from core.config import SECRET_KEY, ALGORITHM, TOKEN_EXPIRE_MINUTES

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str):
    return password_context.hash(password)

def verify_password(unhashed_password: str , hashed_pasword : str):
    return password_context.verify(unhashed_password, hashed_pasword)

def create_access_token(data: dict):
    encode_data = data.copy()
    expire_time= datetime.now(timezone.utc) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    encode_data.update({"expire" : expire_time})
    return jwt.encode(encode_data, SECRET_KEY, algorithm=ALGORITHM)
