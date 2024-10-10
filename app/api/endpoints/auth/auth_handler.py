from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from app.database import handler
from app.database.errors import ElementNotFoundError
from app.schemas.User import User

auth_router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@auth_router.post("users/login", tags=["User auth"])
def login_user(username: str, password: str):
    user_in_db = handler.get_user_by_name(username)
    if not user_in_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    if user_in_db.hashed_password == pwd_context.hash(password):
        return user_in_db
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Bad credentials"
        )


@auth_router.post("/users/register", tags=["User auth"])
def register_user(user: User):
    try:
        user_in_db = handler.get_user_by_name(user.username)
    except ElementNotFoundError:
        user_in_db = None

    if user_in_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    user.hashed_password = pwd_context.hash(user.hashed_password)
    handler.add_user(user)
    return {"message": "User Added successfully"}
