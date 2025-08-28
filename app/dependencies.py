from uuid import UUID
from fastapi import Depends, HTTPException, Request
from fastapi.security.http import HTTPBearer, HTTPAuthorizationCredentials
from sqlmodel import Session, select
from utils import decode_token
from user.schemas import User
from database import get_db


class DecodeToken(HTTPBearer):

    def __init__(self, auto_error=True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        cred: HTTPAuthorizationCredentials = await super().__call__(request)
        id = decode_token(cred.credentials)
        return id


def get_current_user(id: UUID=Depends(DecodeToken()),
                     db: Session=Depends(get_db)):
    """Used to get the current used."""

    user = db.exec(select(User).where(User.id == id)).first()
    if not user:
        raise HTTPException(detail='user not found')
    return user