from sqlmodel import SQLModel,Field,Relationship
from pydantic import EmailStr
from typing import Annotated
import uuid

class BaseUser(SQLModel):
    username:str=Field(unique=True)
    email:EmailStr=Field(unique=True)
    first_name:str
    last_name:str

class User(BaseUser,table=True):
    id:uuid.UUID=Field(primary_key=True,default_factory=uuid.uuid4)
    password:str
    posts:list["Post"]=Relationship(back_populates="author")
    
class CreateUser(BaseUser):
    password:str=Field(min_length=8)

class UpdateUser(SQLModel):
    email:EmailStr|None=None
    first_name:str|None=None
    last_name:str|None=None

from ..post.schemas import Post