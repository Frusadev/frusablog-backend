from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel

from app.dto.media_dto import MediaDTO
from app.dto.posttag_dto import PostTagDTO


class PostCreateDTO(BaseModel):
    title: str
    description: str
    content: str
    published: bool = False
    tags: Optional[List[str]] = None


class PostUpdateDTO(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    tags: Optional[List[str]] = None


class PostDTO(BaseModel):
    post_id: UUID | None
    author_username: str
    created_at: datetime
    title: str
    last_modified: datetime
    modified: bool
    description: str
    content: str
    published: bool
    medias: list[MediaDTO]
    like_count: int
    comments_count: int
    tags: list[PostTagDTO]
