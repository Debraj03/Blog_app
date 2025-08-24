from fastapi import APIRouter,Depends
from ..database import get_db
from .schemas import *
from sqlmodel import select,Session
from ..utils import hash_password,check_password

user_router=APIRouter(prefix="/users",tags=['Users'])

@user_router.get("/")
def all_users(db:Session=Depends(get_db)):
    users=db.exec(select(User)).all()
    return {"All users":users}

@user_router.post("/sign_up")
def signup_user(user_data:CreateUser,db:Session=Depends(get_db)):
    password=user_data.password
    hashed_password=hash_password(password)
    data=user_data.model_dump(exclude='password')
    
    # print(data)
    user=User(**data,password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user