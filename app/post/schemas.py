import uuid
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship


class BasePost(SQLModel):

    title: str = Field(max_length=70)
    content: str


class Post(BasePost, table=True):
    """Schema for the Post table."""

    id: uuid.UUID = Field(primary_key=True, default_factory=uuid.uuid4)
    author_id: uuid.UUID = Field(foreign_key="user.id")
    author: "User" = Relationship(back_populates='posts')
    post_comments: list["Comments"] = Relationship(back_populates='post',
                                                   sa_relationship_kwargs={
                                                       "cascade": "all, delete-orphan",
                                                   })
    created_at: datetime = Field(default_factory=datetime.now)
    

class CreatePost(BasePost):
    pass


class UpdatePost(SQLModel):

    title: str | None = None
    content: str | None = None


# Used to prevent circular import
from user.schemas import User
from comments.schemas import Comments