from fastapi import APIRouter, HTTPException

from app.database.errors import ElementNotFoundError
from app.database.handler import (
    add_user,
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


@user_router.post("/users/")
def create_user(user: User):
    add_user(user)
    return {"message": "User created successfully"}


@user_router.get("/users/")
def read_all_users():
    users = get_all_users()
    return users


@user_router.put("/users/{user_id}")
def update_user(
    user_id: int,
    username: str | None = None,
    password: str | None = None
):
    try:
        edit_user(user_id, username, password)
    except ElementNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User updated successfully"}


@user_router.delete("/users/{user_id}")
def delete_user(user_id: int):
    remove_user(user_id)
    return {"message": "User deleted successfully"}
