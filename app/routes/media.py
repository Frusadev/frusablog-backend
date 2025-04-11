from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from app.db.models import User
from app.db.setup import get_db_session
from app.dto.media_dto import ContentTypeLiteral, MediaCreatedDTO
from app.routes.providers import media_provider
from app.routes.providers.auth_provider import get_current_user

media_router = APIRouter()


@media_router.post("/media", response_model=MediaCreatedDTO)
async def upload_media(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db_session)],
    file: UploadFile = File(...),
    media_type: ContentTypeLiteral = Form(...),
    protected: bool = Form(False),  # Default value outside of Annotated
):
    """Upload a new media file"""
    return await media_provider.upload_media(
        db_session=db_session,
        file=file,
        media_type=media_type,
        protected=protected,
        current_user=current_user,
    )


@media_router.get("/media/{media_id}")
async def get_media(
    current_user: Annotated[User, Depends(get_current_user)],
    db_session: Annotated[Session, Depends(get_db_session)],
    media_id: UUID,
):
    """Get a media file"""
    content, content_type = await media_provider.get_media(
        db_session=db_session,
        media_id=media_id,
        current_user=current_user,
    )
    return StreamingResponse(content=[content], media_type=content_type)
