import jwt
from uuid import UUID
from fastapi import HTTPException,status
from passlib.context import CryptContext
from datetime import datetime,timedelta
from settings import settings


context=CryptContext(schemes=['bcrypt'], deprecated="auto")


def hash_password(password:str):
    """Used to hash a normal password"""

    hashed_password=context.hash(password)
    return hashed_password


def check_password(passwod:str, hashed_password:str):
    """Used to check a normal password with the hased password"""

    state=context.verify(passwod, hashed_password)
    return state


def create_token(data:str, refresh=False):
    """Used to create token (both acess or refersh)"""

    payload={}
    if refresh:
        expire=int((datetime.now()+timedelta(minutes=15)).timestamp())
    else:
        expire=int((datetime.now()+timedelta(minutes=5)).timestamp())

    payload.update({'sub':data, "exp":expire})
    token=jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return token


def decode_token(token:str)->UUID:
    """Used to decode a token"""

    try:
        playload=jwt.decode(token, key=settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except jwt.PyJWTError as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(e)}")
    data=playload.get('sub','')
    return UUID(data)