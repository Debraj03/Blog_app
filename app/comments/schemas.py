import uuid
from datetime import datetime
from sqlmodel import SQLModel,Field,Relationship
from typing import Optional


class CommentsInput(SQLModel):
    content:str


class CommentsInputwithParent(SQLModel):
    content:str
    parent_id:uuid.UUID|None=Field(default=None)


class BaseComments(CommentsInput):
    created_at:datetime=Field(default_factory=datetime.now)
    updated_at:datetime=Field(default_factory=datetime.now)


class Comments(BaseComments,table=True):
    id:uuid.UUID=Field(primary_key=True,default_factory=uuid.uuid4)
    post_id:uuid.UUID=Field(foreign_key='post.id')
    post:"Post"=Relationship(back_populates='post_comments')
    user_id:uuid.UUID=Field(foreign_key='user.id')
    user:"User"=Relationship(back_populates='user_comments')
    parent_id:uuid.UUID=Field(foreign_key='comments.id',nullable=True,default=None)
    parent:Optional["Comments"]=Relationship(back_populates='childs',sa_relationship_kwargs={"remote_side": "Comments.id"})
    childs:list["Comments"]=Relationship(back_populates='parent',sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "single_parent": True
        })


class OutputComment(SQLModel):
    id:uuid.UUID
    post_id:uuid.UUID
    user_id:uuid.UUID
    parent_id:uuid.UUID|None=None
    content:str
    childs:list["OutputComment"]=[]


#Used to prevent circular import
from user.schemas import User
from post.schemas import Post