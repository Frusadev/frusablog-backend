from typing import Annotated, List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Form, Query
from sqlmodel import Session

from app.db.models import User
from app.db.setup import get_db_session
from app.dto.post_dto import PostCreateDTO, PostDTO, PostUpdateDTO
from app.routes.providers import post_provider
from app.routes.providers.auth_provider import get_current_user

post_router = APIRouter()


@post_router.get("/posts", response_model=List[PostDTO])
async def get_posts(
    db_session: Annotated[Session, Depends(get_db_session)],
    user: Annotated[User, Depends(get_current_user)],
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    tags: Optional[List[str]] = Query(None),
    author: Optional[str] = None,
    published_only: bool = True,
):
    """Get all posts with optional filtering"""
    return await post_provider.get_posts(
        db_session=db_session,
        skip=skip,
        limit=limit,
        tags=tags,
        author=author,
        published_only=published_only,
    )


@post_router.get("/posts/{post_id}", response_model=PostDTO)
async def get_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Get a specific post by ID"""
    return await post_provider.get_post(
        db_session=db_session,
        post_id=post_id,
        current_user=current_user,
    )


@post_router.post("/posts", response_model=PostDTO)
async def create_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_data: PostCreateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Create a new post"""
    return await post_provider.create_post(
        db_session=db_session,
        post_data=post_data,
        current_user=current_user,
    )


@post_router.put("/posts/{post_id}", response_model=PostDTO)
async def update_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    post_data: PostUpdateDTO,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Update an existing post"""
    return await post_provider.update_post(
        db_session=db_session,
        post_id=post_id,
        post_data=post_data,
        current_user=current_user,
    )


@post_router.delete("/posts/{post_id}")
async def delete_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Delete a post"""
    return await post_provider.delete_post(
        db_session=db_session,
        post_id=post_id,
        current_user=current_user,
    )


@post_router.post("/posts/{post_id}/like")
async def like_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Like a post"""
    return await post_provider.like_post(
        db_session=db_session,
        post_id=post_id,
        current_user=current_user,
    )


@post_router.delete("/posts/{post_id}/like")
async def unlike_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Unlike a post"""
    return await post_provider.unlike_post(
        db_session=db_session,
        post_id=post_id,
        current_user=current_user,
    )


@post_router.post("/posts/{post_id}/media")
async def add_media_to_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(get_current_user)],
    post_id: UUID,
    media_id: UUID = Form(),
    description: str = Form(),
    is_cover: bool = Form(False),
):
    """Add media to a post"""
    return await post_provider.add_media_to_post(
        db_session=db_session,
        post_id=post_id,
        media_id=media_id,
        description=description,
        is_cover=is_cover,
        current_user=current_user,
    )


@post_router.delete("/posts/{post_id}/media/{media_id}")
async def remove_media_from_post(
    db_session: Annotated[Session, Depends(get_db_session)],
    post_id: UUID,
    media_id: UUID,
    current_user: Annotated[User, Depends(get_current_user)],
):
    """Remove media from a post"""
    return await post_provider.remove_media_from_post(
        db_session=db_session,
        post_id=post_id,
        media_id=media_id,
        current_user=current_user,
    )
