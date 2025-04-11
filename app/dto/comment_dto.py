from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class CommentCreateDTO(BaseModel):
    post_id: UUID
    content: str


class CommentUpdateDTO(BaseModel):
    content: str


class CommentDTO(BaseModel):
    comment_id: Optional[UUID]
    post_id: UUID
    author_username: str
    created_at: datetime
    last_modified: datetime
    modified: bool
    content: str
    likes_count: int
