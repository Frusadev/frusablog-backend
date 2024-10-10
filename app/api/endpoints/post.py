from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.database.errors import ElementNotFoundError
from app.database.handler import (
    add_post,
    edit_post,
    get_all_posts,
    get_post,
    get_posts_by_user,
    remove_post,
)
from app.schemas.Post import Post
from app.schemas.User import User

post_router = APIRouter()


@post_router.get("/posts/{post_id}", response_model=Post)
def read_post(post_id: int):
    try:
        post = get_post(post_id)
        return post
    except ElementNotFoundError:
        raise HTTPException(status_code=404, detail="Post not found")


@post_router.post("/posts/{user_id}")
def create_post(
    user_id: int, post: Post, user: Annotated[User, Depends(get_current_user)]
):
    if not user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    add_post(user_id, post)
    return {"message": "Post created successfully"}


@post_router.get("/posts/")
def read_all_posts():
    posts = get_all_posts()
    return posts


@post_router.get("/posts/user/{user_id}")
def read_posts_by_user(user_id: int):
    posts = get_posts_by_user(user_id)
    return posts


@post_router.put("/posts/{post_id}")
def update_post(
    post_id: int, content: str, user: Annotated[User, Depends(get_current_user)]
):
    post = get_post(post_id)
    if not post.user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    edit_post(post_id, content)
    return {"message": "Post updated successfully"}


@post_router.delete("/posts/{post_id}")
def delete_post(post_id: int, user: Annotated[User, Depends(get_current_user)]):
    post = get_post(post_id)
    if not post.user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    remove_post(post_id)
    return {"message": "Post deleted successfully"}
