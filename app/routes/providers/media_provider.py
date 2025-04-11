import uuid

from fastapi import HTTPException, UploadFile
from sqlmodel import Session
from starlette.status import HTTP_400_BAD_REQUEST

from app.db.models import Media, User
from app.dto.media_dto import ContentTypeLiteral, MediaCreatedDTO
from app.storage.storage import get_file, write_file


async def upload_media(
    db_session: Session,
    file: UploadFile,
    media_type: ContentTypeLiteral,
    protected: bool,
    current_user: User,
):
    """Upload a new media file"""
    # Validate file type
    if not file.size:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="File size is required",
        )

    if file.size > 5 * 1024 * 1024:
        ...
    if not file.filename:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    # Create media record
    media = Media(
        name=file.filename,
        protected=protected,
        media_type=media_type,
        description=file.filename,
        uploader_username=current_user.username,
    )

    db_session.add(media)

    # Save file using storage utility
    try:
        write_file(file, media)
    except Exception as e:
        # If file saving fails, clean up the DB record
        db_session.rollback()
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Failed to save file: {str(e)}",
        )

    db_session.commit()
    db_session.refresh(media)

    return MediaCreatedDTO(url=f"/v1/media/{media.media_id}")


async def get_media(
    db_session: Session, media_id: uuid.UUID, current_user: User
):
    """Get a media file"""
    media = db_session.get(Media, media_id)
    if not media:
        raise HTTPException(status_code=404, detail="Media not found")

    # Check if media is protected and user is logged in
    if media.protected and not current_user:
        raise HTTPException(status_code=403, detail="Media is protected")

    try:
        content = get_file(media)
        return content, media.media_type
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="Media file not found")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to retrieve media: {str(e)}"
        )
