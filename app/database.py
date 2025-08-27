from sqlmodel import SQLModel,create_engine,Session
from .settings import settings


connect_args={"check_same_thread":False}

engine=create_engine(settings.DB_URL, connect_args=connect_args, echo=True)


def create_db_and_tables():
    """Used to create all the databases and tables"""

    SQLModel.metadata.create_all(engine)


def get_db():
    """Used to get the database session connection"""
    
    with Session(engine) as db:
        yield db