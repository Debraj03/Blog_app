from fastapi import APIRouter,Depends,status,HTTPException
from .schemas import *
from sqlmodel import Session,select
from ..database import get_db
from ..dependencies import get_current_user

post_router=APIRouter(prefix='/posts',tags=['Post'])

@post_router.get('/',status_code=status.HTTP_200_OK)
def get_all_posts(db:Session=Depends(get_db)):
    posts=db.exec(select(Post).order_by(Post.created_at.desc())).all()
    return posts

@post_router.get('/{post_id}',status_code=status.HTTP_200_OK)
def get_all_posts(post_id:uuid.UUID,db:Session=Depends(get_db)):
    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    return post

@post_router.post('/',status_code=status.HTTP_201_CREATED)
def create_post(post_data:CreatePost,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    data=post_data.model_dump()
    try:
        post=Post(**data,author_id=user.id,author=user)
        db.add(post)
        db.commit()
        db.refresh(post)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={"Error":str(e)})
    return post

@post_router.put('/{post_id}',status_code=status.HTTP_202_ACCEPTED)
def update_post(post_id:uuid.UUID,post_data:UpdatePost,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    if post.author_id!=user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unauthorized to update this post")
    data=post_data.model_dump(exclude_unset=True)
    try:
        post=post.sqlmodel_update(data)
        db.add(post)
        db.commit()
        db.refresh(post)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={"Error":str(e)})
    return post

@post_router.delete('/{post_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id:uuid.UUID,user:User=Depends(get_current_user),db:Session=Depends(get_db)):
    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    if post.author_id!=user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are Unauthorized to delete this post")
    try:
        
        db.delete(post)
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,detail={"Error":str(e)})
    return {"detail":"post deleted sucessfully"}