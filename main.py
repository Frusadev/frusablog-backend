from fastapi import FastAPI

from app.api.endpoints.post import post_router
from app.api.endpoints.user import user_router
from app.api.endpoints.comment import comment_router
from app.api.endpoints.auth.auth_handler import auth_router

app = FastAPI()
app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)
app.include_router(auth_router)
