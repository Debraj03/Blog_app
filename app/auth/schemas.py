from sqlmodel import SQLModel


class Login(SQLModel):
    """Schema for the login data."""

    username: str
    password: str