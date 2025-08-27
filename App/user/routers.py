from fastapi import APIRouter,Depends,status,HTTPException
from sqlmodel import select,Session
from ..database import get_db
from .schemas import User,OutputUser,UpdateUser
from ..dependencies import get_current_user


# Creting the user router
user_router=APIRouter(prefix="/users",tags=['Users'])


@user_router.get('',response_model=list[OutputUser],status_code=status.HTTP_200_OK)
def all_users(db:Session=Depends(get_db)):
    """Used to get all the users"""

    users=db.exec(select(User)).all()
    return users


@user_router.put('/upadte_profile',response_model=OutputUser,status_code=status.HTTP_202_ACCEPTED)
def update_user_profile(user_data:UpdateUser,
                        user:User=Depends(get_current_user),
                        db:Session=Depends(get_db)):
    
    """Used to update the profile details of user"""

    user_data=user_data.model_dump(exclude_unset=True)
    updated_user=user.sqlmodel_update(user_data)
    try:
        db.add(updated_user)
        db.commit()
        db.refresh(updated_user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'error':str(e)})
    return updated_user


@user_router.get('/profile',status_code=status.HTTP_200_OK)
def get_present_user(user:User=Depends(get_current_user)):
    """Used to get the current user details"""

    return user