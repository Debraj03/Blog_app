from sqlmodel import SQLModel,Field,Relationship
import uuid
from datetime import datetime
class BasePost(SQLModel):
    title:str=Field(max_length=70)
    content:str
    created_at:datetime=Field(default_factory=datetime.now)
class Post(BasePost,table=True):
    id:uuid.UUID=Field(primary_key=True,default_factory=uuid.uuid4)
    author_id:uuid.UUID=Field(foreign_key="user.id")
    author:"User"=Relationship(back_populates='posts')

class CreatePost(BasePost):
    pass

from ..user.schemas import User