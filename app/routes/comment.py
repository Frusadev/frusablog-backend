from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.db.models import User
from app.db.setup import get_db_session
from app.dto.comment_dto import CommentCreateDTO, CommentDTO, CommentUpdateDTO
from app.routes.providers import comment_provider
from app.routes.providers.auth_provider import get_current_user

comment_router = APIRouter()


@comment_router.get("/comments/{comment_id}", response_model=CommentDTO)
async def get_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    _user: Annotated[User, Depends(get_current_user)],
    comment_id: UUID,
):
    """Get a specific comment by ID"""
    return await comment_provider.get_comment(
        db_session=db_session,
        comment_id=comment_id,
    )


@comment_router.post("/comments", response_model=CommentDTO)
async def create_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    comment_data: CommentCreateDTO,
    current_user: User = Depends(get_current_user),
):
    """Create a new comment on a post"""
    return await comment_provider.create_comment(
        db_session=db_session,
        comment_data=comment_data,
        current_user=current_user,
    )


@comment_router.put("/comments/{comment_id}", response_model=CommentDTO)
async def update_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    comment_id: UUID,
    comment_data: CommentUpdateDTO,
    current_user: User = Depends(get_current_user),
):
    """Update an existing comment"""
    return await comment_provider.update_comment(
        db_session=db_session,
        comment_id=comment_id,
        comment_data=comment_data,
        current_user=current_user,
    )


@comment_router.delete("/comments/{comment_id}")
async def delete_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
):
    """Delete a comment"""
    return await comment_provider.delete_comment(
        db_session=db_session,
        comment_id=comment_id,
        current_user=current_user,
    )


@comment_router.post("/comments/{comment_id}/like")
async def like_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
):
    """Like a comment"""
    return await comment_provider.like_comment(
        db_session=db_session,
        comment_id=comment_id,
        current_user=current_user,
    )


@comment_router.delete("/comments/{comment_id}/like")
async def unlike_comment(
    db_session: Annotated[Session, Depends(get_db_session)],
    comment_id: UUID,
    current_user: User = Depends(get_current_user),
):
    """Unlike a comment"""
    return await comment_provider.unlike_comment(
        db_session=db_session,
        comment_id=comment_id,
        current_user=current_user,
    )
