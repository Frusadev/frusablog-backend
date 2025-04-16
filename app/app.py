import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import env
from app.routes.auth import auth_router
from app.routes.comment import comment_router
from app.routes.media import media_router
from app.routes.post import post_router
from app.routes.posttag import posttag_router
from app.routes.user import user_router

API_VERSION = env.get_env("API_VERSION", "/v1")

app = FastAPI()
app.include_router(auth_router, prefix=API_VERSION)
app.include_router(post_router, prefix=API_VERSION)
app.include_router(comment_router, prefix=API_VERSION)
app.include_router(media_router, prefix=API_VERSION)
app.include_router(posttag_router, prefix=API_VERSION)
app.include_router(user_router, prefix=API_VERSION)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000"
    ],  # Or ["http://localhost:3000"] for stricter control
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DEBUG = env.get_env("DEBUG", "True").lower() == "true"


@app.get("/")
def read_root():
    return {"message": "Hello World"}


def run_app():
    if DEBUG:
        uvicorn.run(
            "app:app",
            reload=True,
            host="0.0.0.0",
            port=int(env.get_env("PORT", "8000")),
        )
    else:
        uvicorn.run(app, host="0.0.0.0", port=int(env.get_env("PORT", "8000")))
