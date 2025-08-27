from fastapi import APIRouter,Depends,HTTPException,status
from sqlmodel import Session,select
from user.schemas import User,CreateUser
from database import get_db
from utils import hash_password,check_password,create_token,decode_token
from .schemas import Login


# Creating the auth router
auth_router=APIRouter(prefix='/auth',tags=['Auth'])


@auth_router.post("/signup",status_code=status.HTTP_200_OK)
def signup_user(user_data:CreateUser,
                db:Session=Depends(get_db)):
    
    """Used to register a user"""

    password=user_data.password
    hashed_password=hash_password(password)
    data=user_data.model_dump(exclude='password')
    user=User(**data,password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@auth_router.post("/login",status_code=status.HTTP_200_OK)
def user_login(login_data:Login,
               db:Session=Depends(get_db)):
    
    """Used to login a user it generates a access token and a refresh token
    after verifing the used creadentials"""

    user=db.exec(select(User).where(User.username==login_data.username)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'error':'user not found'}) 
    if not check_password(login_data.password,user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={'error':'invalid password'}) 
    acess_token=create_token(data=str(user.id))
    refresh_token=create_token(data=str(user.id),refresh=True)
    return {"acess_token":acess_token,"refresh_token":refresh_token}


@auth_router.get('/refresh_token/{refresh_token}',status_code=status.HTTP_200_OK)
def generate_acess_token_from_refresh_token(refresh_token:str):
    """Generates a acess token from a refresh token afer verifing the refresh token"""

    id=decode_token(refresh_token)
    acess_token=create_token(data=str(id))
    return {'acess_token':acess_token}