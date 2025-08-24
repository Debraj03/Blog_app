from fastapi import APIRouter,Depends
from ..database import get_db
from .schemas import *
from sqlmodel import select,Session
from ..utils import hash_password,check_password
from ..dependencies import get_current_user

user_router=APIRouter(prefix="/users",tags=['Users'])

@user_router.get("/")
def all_users(db:Session=Depends(get_db)):
    users=db.exec(select(User)).all()
    return {"All users":users}

@user_router.get("/me")
def get_present_user(user:User=Depends(get_current_user)):
    return user