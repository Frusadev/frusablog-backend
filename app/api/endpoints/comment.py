from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.database.errors import ElementNotFoundError
from app.database.handler import (
    add_comment,
    edit_comment,
    get_all_comments,
    get_comment,
    get_comments_by_post,
    get_comments_by_user,
    remove_comment,
)
from app.schemas.Comment import Comment
from app.schemas.User import User

comment_router = APIRouter()


@comment_router.get("/comments/{comment_id}", response_model=Comment)
def read_comment(comment_id: int):
    try:
        comment = get_comment(comment_id)
        return comment
    except ElementNotFoundError:
        raise HTTPException(status_code=404, detail="Comment not found")


@comment_router.get("/comments/")
def read_all_comments():
    comments = get_all_comments()
    return comments


@comment_router.get("/comments/post/{post_id}")
def read_comments_by_post(post_id: int):
    comments = get_comments_by_post(post_id)
    return comments


@comment_router.get("/comments/user/{user_id}")
def read_comments_by_user(user_id: int):
    comments = get_comments_by_user(user_id)
    return comments


@comment_router.put("/comments/{comment_id}")
def update_comment(
    comment_id: int, content: str, user: Annotated[User, Depends(get_current_user)]
):
    comment = get_comment(comment_id)
    if not comment.user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    edit_comment(comment_id, content)
    return {"message": "Comment updated successfully"}


@comment_router.delete("/comments/{comment_id}")
def delete_comment(comment_id: int, user: Annotated[User, Depends(get_current_user)]):
    comment = get_comment(comment_id)
    if not comment.user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    remove_comment(comment_id)
    return {"message": "Comment deleted successfully"}


@comment_router.post("/comments/{user_id}/{post_id}")
def create_comment(
    user_id: int,
    post_id: int,
    comment: Comment,
    user: Annotated[User, Depends(get_current_user)],
):
    if not user_id == user.user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    add_comment(user_id, post_id, comment)
    return {"message": "Comment created successfully"}
