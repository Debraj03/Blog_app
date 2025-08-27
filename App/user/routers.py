from fastapi import APIRouter,Depends,status
from sqlmodel import select,Session
from ..database import get_db
from .schemas import User,OutputUser
from ..dependencies import get_current_user


# Creting the user router
user_router=APIRouter(prefix="/users",tags=['Users'])


@user_router.get('',response_model=list[OutputUser],status_code=status.HTTP_200_OK)
def all_users(db:Session=Depends(get_db)):
    """Used to get all the users"""

    users=db.exec(select(User)).all()
    return users


@user_router.get('/me',status_code=status.HTTP_200_OK)
def get_present_user(user:User=Depends(get_current_user)):
    """Used to get the current user"""

    return user