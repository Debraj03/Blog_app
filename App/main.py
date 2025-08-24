from fastapi import FastAPI
from .user.routers import user_router
from .auth.routers import auth_router
from .database import create_db_and_tables
app=FastAPI()

@app.on_event('startup')
def startup_event():
    create_db_and_tables()

@app.get("/")
def home():
    return{"Hello":"World"}

app.include_router(user_router)
app.include_router(auth_router)