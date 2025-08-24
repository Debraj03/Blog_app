from fastapi import APIRouter,Depends
from .schemas import *
from sqlmodel import Session,select
from ..database import get_db
from ..dependencies import get_current_user

post_router=APIRouter(prefix='/posts',tags=['Post'])

@post_router.get('/')
def get_all_posts(db:Session=Depends(get_db)):
    posts=db.exec(select(Post).order_by(Post.created_at.desc())).all()
    return posts

@post_router.post('/create')
def create_post(post_data:CreatePost,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    data=post_data.model_dump()
    post=Post(**data,author_id=user.id,author=user)
    print(post)
    db.add(post)
    db.commit()
    db.refresh(post)
    return post