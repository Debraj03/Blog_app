from fastapi import HTTPException,status
from passlib.context import CryptContext
import jwt
from .settings import settings
from datetime import datetime,timedelta
from uuid import UUID

context=CryptContext(schemes=['bcrypt'],deprecated="auto")

def hash_password(password:str):
    hashed_password=context.hash(password)
    return hashed_password

def check_password(passwod:str,hashed_password:str):
    state=context.verify(passwod,hashed_password)
    return state

def create_token(data:str,refresh=False):
    payload={}
    if refresh:
        expire=int((datetime.now()+timedelta(minutes=15)).timestamp())
    else:
        expire=int((datetime.now()+timedelta(minutes=5)).timestamp())

    payload.update({'sub':data,"exp":expire})
    token=jwt.encode(payload=payload,key=settings.SECRET_KEY,algorithm=settings.ALGORITHM)
    return token

def decode_token(token:str)->UUID:
    try:
        playload=jwt.decode(token,key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"{str(e)}")
    data=playload.get('sub','')
    return UUID(data)