from datetime import datetime, timedelta, timezone
from typing import Annotated

from fastapi import Cookie, Depends, Form, HTTPException, Response
from fastapi.responses import RedirectResponse
from pydantic import EmailStr
from sqlmodel import Session, select
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)

from app.config import env
from app.db.models import AuthSession, LoginSession, Role, User
from app.db.setup import get_db_session
from app.log.console import log_info
from app.miscellaneous.error_codes import (
    ERR_INVALID_CREDENTIALS,
    ERR_NEED_VERIFICATION,
)
from app.security.password import hash_password, verify_password
from app.services.email import send_templated_email
from app.utils.crypto import gen_id

ACCOUNT_VERIFICATION_URL = env.get_env(
    "ACCOUNT_VERIFICATION_URL",
    "https://api.ametsowou.me/v1/auth/verify",
)


APP_EMAIL_ADDRESS = env.get_env("APP_EMAIL_ADDRESS", "")


async def register(
    db_session: Annotated[Session, Depends(get_db_session)],
    email: Annotated[EmailStr, Form()],
    username: Annotated[str, Form()],
    display_name: Annotated[str, Form()],
    password: Annotated[str, Form()],
    password_repeat: Annotated[str, Form()],
):
    """
    Register a new user.
    Args:
        db_session (Session): The database session.
        email (EmailStr): The user's email.
        username (str): The user's username.
        display_name (str): The user's display name.
        password (str): The user's password.
        password_repeat (str): The user's password repeat.
    """
    if not password == password_repeat:
        raise ValueError("Passwords do not match")

    user_in_db = db_session.get(User, username)
    if user_in_db:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT, detail="Username taken."
        )
    stmt = select(User).where(User.email == email)
    user_in_db = db_session.exec(stmt).first()
    if user_in_db:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="Email used.",
        )
    role = Role(role_id=gen_id(), role_type="user")
    user = User(
        username=username,
        email=email,
        display_name=display_name,
        hashed_password=hash_password(password),
        role_id=role.role_id,
        avatar_url=None,
        last_login=datetime.utcnow(),
        bio=None,
        work_industry=None,
        work_title=None,
        location=None,
    )
    auth_session = AuthSession(
        username=username,
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(minutes=30),
    )
    db_session.add(role)
    db_session.add(user)
    db_session.add(auth_session)
    db_session.commit()
    db_session.refresh(user)
    print(ACCOUNT_VERIFICATION_URL)
    send_templated_email(
        email=user.email,
        subject="Thank you for joining me.",
        context={
            "user_name": user.display_name,
            "verification_link": f"{ACCOUNT_VERIFICATION_URL}?token={auth_session.session_id}",
            "github_link": "https://github.com/Frusadev",
            "linkedin_link": "https://www.linkedin.com/in/frusadev",
            "current_year": datetime.utcnow().year,
            "unsubscribe_link": "https://blog.ametsowou.me/unsubscribe",
            "preference_link": "https://blog.ametsowou.me/account/preferences",
        },
        template_name="welcome",
        fallback_message=f"Hello {user.display_name},\n\n here is your verification link: {ACCOUNT_VERIFICATION_URL}?token={auth_session.session_id}",
    )
    log_info(f"Registerd new user: {user.username}: {user.email}")


async def login(
    db_session: Annotated[Session, Depends(get_db_session)],
    email: Annotated[EmailStr, Form()],
    password: Annotated[str, Form()],
    response: Response,
):
    """
    Login a user and create a session.
    If the user is not verified, send a verification email.
    Args:
        db_session (Session): The database session.
        email (EmailStr): The user's email.
        password (str): The user's password.
        response (Response): The response object.
    Returns:
        UserDTO: The logged-in user.
    """
    stmt = select(User).where(User.email == email)
    user = db_session.exec(stmt).first()
    if not user:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=ERR_INVALID_CREDENTIALS,
        )

    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=ERR_INVALID_CREDENTIALS,
        )

    if (
        not user.account_verified
        or user.last_login < datetime.utcnow() - timedelta(days=170)
    ):
        auth_session = AuthSession(
            username=user.username,
            issued_at=datetime.utcnow(),
            expires_at=datetime.utcnow() + timedelta(minutes=30),
        )
        db_session.add(auth_session)
        db_session.commit()
        send_templated_email(
            email=user.email,
            template_name="verification",
            context={
                "user_name": user.display_name,
                "verification_link": f"{ACCOUNT_VERIFICATION_URL}?token={auth_session.session_id}",
                "expiry_time": "30",
                "contact_email": APP_EMAIL_ADDRESS,
                "current_year": datetime.utcnow().year,
            },
            subject="Account verification",
            fallback_message=f"Hello {user.display_name},\n\n here is your verification link: {ACCOUNT_VERIFICATION_URL}?token={user.username}",
        )

        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail=ERR_NEED_VERIFICATION,
        )

    login_session = LoginSession(
        username=user.username,
        issued_at=datetime.utcnow(),
        expires_at=datetime.utcnow() + timedelta(days=365),
    )
    db_session.add(login_session)
    db_session.commit()
    db_session.refresh(login_session)
    response.set_cookie(
        key="session",
        value=login_session.session_id,
        httponly=True,
        expires=datetime.now(timezone.utc)
        + timedelta(days=364)
        + timedelta(hours=23),
    )
    log_info(f"User {user.username} logged in.")
    return user.to_dto()


async def verify_auth_session(
    db_session: Annotated[Session, Depends(get_db_session)], session_id: str
):
    """
    Verify the authentication session.
    Args:
        db_session (Session): The database session.
        session_id (str): The session ID.
    Returns:
        AuthSession: The authenticated session.
    """
    auth_session = db_session.get(AuthSession, session_id)
    if not auth_session or auth_session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Session expired.",
        )
    user = auth_session.user
    user.account_verified = True
    user.last_login = datetime.utcnow()
    db_session.add(user)
    db_session.delete(auth_session)
    db_session.commit()
    return RedirectResponse(
        url=f"{env.get_env('DOMAIN', default_value='https://blog.ametsowou.me')}/login"
    )


async def get_current_user(
    db_session: Annotated[Session, Depends(get_db_session)],
    session: Annotated[str | None, Cookie()] = None,
):
    """
    Get the current user from the session cookie.
    """
    if not session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
        )
    login_session = db_session.get(LoginSession, session)
    if not login_session or login_session.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user = db_session.get(User, login_session.username)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    user.last_login = datetime.utcnow()
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user


async def logout(
    db_session: Annotated[Session, Depends(get_db_session)],
    response: Response,
    session: str | None,
):
    """
    Logout the user by deleting the session cookie.
    Args:
        db_session (Session): The database session.
        response (Response): The response object.
        session (str | None): The session ID from the cookie.
    """
    if not session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    login_session = db_session.get(LoginSession, session)
    if not login_session:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    db_session.delete(login_session)
    db_session.commit()
    response.delete_cookie("session")
    log_info(f"User {login_session.username} logged out.")
