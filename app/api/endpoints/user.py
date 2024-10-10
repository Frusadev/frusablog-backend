from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_current_user
from app.database.errors import ElementNotFoundError
from app.database.handler import (
    edit_user,
    get_all_users,
    get_user,
    remove_user,
)
from app.schemas.User import User

user_router = APIRouter()


@user_router.get("/users/{user_id}", response_model=User)
def read_user(user_id: int):
    try:
        user = get_user(user_id)
        return user
    except ElementNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")


@user_router.get("/users/", response_model=list[User])
def read_all_users():
    users = get_all_users()
    return users


@user_router.put("/users/{user_id}")
def update_user(
    user: Annotated[User, Depends(get_current_user)],
    user_id: int,
    username: str | None = None,
    password: str | None = None
):
    if not user.user_id == user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    try:
        edit_user(user_id, username, password)
    except ElementNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@user_router.delete("/users/")
def delete_user(user: Annotated[User, Depends(get_current_user)]):
    assert user.user_id is not None, "User_id must be defined"
    remove_user(user.user_id)
    return {"message": "User deleted successfully"}
