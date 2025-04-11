from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Form, Response
from pydantic import EmailStr, StringConstraints, constr
from sqlmodel import Session

from app.db.setup import get_db_session
from app.routes.providers import auth_provider

auth_router = APIRouter()

AlphaNumericalStr = constr()


@auth_router.post("/auth/register")
async def register(
    db_session: Annotated[Session, Depends(get_db_session)],
    email: Annotated[EmailStr, Form()],
    username: Annotated[
        Annotated[str, Form()],
        StringConstraints(
            max_length=15, min_length=5, pattern=r"^[a-z0-9_]+$"
        ),
    ],
    display_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_repeat: Annotated[str, Form()],
):
    return await auth_provider.register(
        db_session=db_session,
        email=email,
        username=username,
        display_name=display_name,
        password=password,
        password_repeat=password_repeat,
    )


@auth_router.post("/auth/login")
async def login(
    db_session: Annotated[Session, Depends(get_db_session)],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    response: Response,
):
    return await auth_provider.login(
        db_session=db_session,
        email=email,
        password=password,
        response=response,
    )


@auth_router.post("/auth/logout")
async def logout(
    db_session: Annotated[Session, Depends(get_db_session)],
    response: Response,
    session: Annotated[str | None, Cookie()] = None,
):
    return await auth_provider.logout(
        db_session=db_session,
        response=response,
        session=session,
    )


@auth_router.get("/auth/verify")
async def verify(
    db_session: Annotated[Session, Depends(get_db_session)],
    token: str,
):
    return await auth_provider.verify_auth_session(
        db_session=db_session,
        session_id=token,
    )
