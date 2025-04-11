from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.models import Post, User
from app.db.setup import get_db_session
from app.dto.user_dto import UserDTO
from app.routes.providers import user_provider
from app.routes.providers.auth_provider import get_current_user

user_router = APIRouter()


@user_router.get("/{username}/posts", response_model=List[Post])
async def read_user_posts(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db_session)],
    username: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = Query(True),
):
    """Get all posts by a specific user"""
    posts = await user_provider.get_user_posts(
        db_session=db_session,
        current_user=current_user,
        username=username,
        skip=skip,
        limit=limit,
        published_only=published_only,
    )
    return posts


@user_router.get("/user/{username}", response_model=UserDTO)
async def read_user_profile(
    username: str,
    db_session: Annotated[Session, Depends(get_db_session)],
):
    """Get a user's public profile"""
    profile = await user_provider.get_user_profile(
        db_session=db_session,
        username=username,
    )
    return profile


@user_router.get("/me/email", response_model=str)
async def read_user_email(
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get the current user's email address"""
    email = await user_provider.get_user_email(
        db_session=db_session,
        user=current_user,
    )
    return email


@user_router.put("/me/industry", response_model=UserDTO)
async def update_work_industry(
    industry: user_provider.WorkIndustries,
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update the current user's work industry"""
    updated_user = await user_provider.change_work_industry(
        db_session=db_session,
        user=current_user,
        industry=industry,
    )
    return updated_user


@user_router.put("/me/bio", response_model=UserDTO)
async def update_bio(
    bio: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update the current user's bio"""
    updated_user = await user_provider.change_bio(
        db_session=db_session,
        user=current_user,
        bio=bio,
    )
    return updated_user


@user_router.put("/me/location", response_model=UserDTO)
async def update_location(
    location: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update the current user's location"""
    updated_user = await user_provider.change_location(
        db_session=db_session,
        user=current_user,
        location=location,
    )
    return updated_user


@user_router.put("/me/work-title", response_model=UserDTO)
async def update_work_title(
    title: str,
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update the current user's work title"""
    updated_user = await user_provider.change_work_title(
        db_session=db_session,
        user=current_user,
        title=title,
    )
    return updated_user


@user_router.post("/account/unsubscribe")
async def unsubscribe(
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Unsubscribe the current user"""
    return await user_provider.unsubscribe(
        db_session=db_session,
        user=current_user,
    )


@user_router.delete("/account/delete")
async def delete_account(
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete the current user's account"""
    return await user_provider.delete_user(
        db_session=db_session,
        user=current_user,
    )


@user_router.get("/me", response_model=UserDTO)
async def current_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get the current user's profile"""
    profile = await user_provider.get_current_user(user=current_user)
    return profile
