import uuid
from datetime import datetime
from fastapi import APIRouter,HTTPException,status,Depends
from sqlmodel import Session,select,col
from .schemas import Comments,OutputComment,CommentsInput,CommentsInputwithParent
from ..post.schemas import Post
from ..user.schemas import User
from ..dependencies import get_current_user
from ..database import get_db


# Creating the commnets router
comment_router=APIRouter(prefix='/posts',tags=['comments'])


@comment_router.get('/{post_id}/comments',response_model=list[OutputComment],status_code=status.HTTP_200_OK)
def get_all_comments_for_a_post(post_id:uuid.UUID,
                                db:Session=Depends(get_db)):
    
    """Used to get all the comments for a particular post"""

    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"error":f"post with id {post_id} not found"})
    comments=db.exec(select(Comments).where(Comments.post_id==post_id,col(Comments.parent_id).is_(None))).all()
    return comments


@comment_router.post('/{post_id}/comments',response_model=OutputComment,status_code=status.HTTP_201_CREATED)
def create_comment(post_id:uuid.UUID,
                   comment_data:CommentsInputwithParent,
                   user:User=Depends(get_current_user),
                   db:Session=Depends(get_db)):
    
    """Used to create a commnet on a post using the post id"""

    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"error":f"post with id {post_id} not found"})
    parent_id=comment_data.parent_id
    if parent_id:
        parent=db.exec(select(Comments).where(Comments.id==parent_id,Comments.post_id==post_id)).first()
        if not parent:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail={'error':'parent_id not found'})
    data=comment_data.model_dump()
    comment=Comments(**data,user=user,user_id=user.id,post=post,post_id=post.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@comment_router.put('/{post_id}/comments/{comment_id}',response_model=OutputComment,status_code=status.HTTP_202_ACCEPTED)
def update_comment(post_id:uuid.UUID,
                   comment_id:uuid.UUID,
                   comment_data:CommentsInput,
                   user:User=Depends(get_current_user),
                   db:Session=Depends(get_db)):
    
    """Used to update a comment using the post id and the comment id
    only the author of the comment can update the comment"""

    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    comment=db.exec(select(Comments).where(Comments.id==comment_id,Comments.post_id==post_id)).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"error":"comment not found"})
    if comment.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={"error":"You are unauthorized to edit this comment"})
    data=comment_data.model_dump()
    data.update({'updated_at':datetime.now()})
    comment=comment.sqlmodel_update(data)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@comment_router.delete('/{post_id}/comments/{comment_id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(post_id:uuid.UUID,
                   comment_id:uuid.UUID,
                   user:User=Depends(get_current_user),
                   db:Session=Depends(get_db)):
    
    """Used to delete a post using the post id and the commnet id
    only the author of the commnet can delete the comment"""

    post=db.exec(select(Post).where(Post.id==post_id)).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id {post_id} not found")
    comment=db.exec(select(Comments).where(Comments.id==comment_id,Comments.post_id==post_id)).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail={"error":"comment not found"})
    if comment.user_id!=user.id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail={"error":"You are unauthorized to delete this comment"})
    db.delete(comment)
    db.commit()
    return {'message':'Comment deleted sucessfully'}