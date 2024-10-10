from fastapi import FastAPI

from app.api.endpoints.post import post_router
from app.api.endpoints.user import user_router
from app.api.endpoints.comment import comment_router
from app.api.endpoints.auth.auth_handler import auth_router
from fastapi.middleware.cors import CORSMiddleware

routers = [
    user_router,
    post_router,
    comment_router,
    auth_router
]

origins = [
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods="*",
    allow_headers="*",
)

for router in routers:
    app.include_router(router)
