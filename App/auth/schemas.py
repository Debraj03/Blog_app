from sqlmodel import SQLModel,Field


class Login(SQLModel):
    username:str
    password:str