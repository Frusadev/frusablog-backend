from typing import Literal, Optional
from uuid import UUID

from pydantic import BaseModel

ContentTypeLiteral = Literal[
    # Images
    "image/jpeg",
    "image/png",
    "image/webp",
    "image/gif",
    "image/svg+xml",
    "image/bmp",
    "image/tiff",
    # Videos
    "video/mp4",
    "video/webm",
    "video/ogg",
    "video/quicktime",
    "video/x-msvideo",
    "video/x-matroska",
    # Audio
    "audio/mpeg",
    "audio/ogg",
    "audio/wav",
    "audio/webm",
    "audio/aac",
    "audio/flac",
    # Documents
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.ms-powerpoint",
    "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "text/plain",
    "text/csv",
    "text/html",
    "application/json",
    "application/xml",
    # Archives
    "application/zip",
    "application/x-tar",
    "application/x-7z-compressed",
    "application/x-rar-compressed",
    "other",
]


class MediaDTO(BaseModel):
    media_id: Optional[UUID]
    name: str
    protected: bool
    description: Optional[str]
    content_type: str


class MediaCreateDTO(BaseModel):
    name: str
    protected: bool = False
    description: Optional[str]
    content_type: ContentTypeLiteral


class MediaCreatedDTO(BaseModel):
    url: str


class PostMedia(BaseModel):
    media_id: Optional[UUID]
    post_id: Optional[UUID]
    description: str
    cover_image: bool = False  # If false, will be considered as an attachment.
