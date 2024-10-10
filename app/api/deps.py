from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from passlib.context import CryptContext

from app.database import handler
from app.api.endpoints.settings import ALGORITHM, SECRET_KEY
from app.schemas.User import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def create_access_token(data: dict, expiration_duration: timedelta | None = None):
    expire = datetime.now(timezone.utc) + timedelta(days=30)
    if expiration_duration:
        expire = datetime.now(timezone.utc) + expiration_duration
    encoding_data = data.copy()
    encoding_data.update({"exp": expire})
    token = jwt.encode(encoding_data, key=SECRET_KEY, algorithm=ALGORITHM)
    return {"token": token}


async def authenticate_token(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Bad credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            raise credentials_exception
        user = handler.get_user_by_name(username)
        if not user:
            raise credentials_exception
        return user
    except InvalidTokenError:
        raise credentials_exception


async def get_current_user(user: Annotated[User, Depends(authenticate_token)]):
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
