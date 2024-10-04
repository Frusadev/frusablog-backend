from fastapi import FastAPI

from app.endpoints.post import post_router
from app.endpoints.user import user_router
from app.endpoints.comment import comment_router
from app.endpoints.auth import auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(auth_router)
