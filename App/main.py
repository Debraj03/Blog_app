from fastapi import FastAPI
from .user.routers import user_router
from .auth.routers import auth_router
from .post.routers import post_router
from .comments.routers import comment_router
from .database import create_db_and_tables


app=FastAPI(title="Blog App",
            description="This is a Blog app api where you can post your blogs and read or create commnets on them")


@app.on_event('startup')
def startup_event():
    create_db_and_tables()


@app.get("/",tags=["Index"])
def home():
    return{"Hello":"World"}


# Including all the routers
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(post_router)
app.include_router(comment_router)