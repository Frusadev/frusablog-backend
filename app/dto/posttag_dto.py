from uuid import UUID
from pydantic import BaseModel


class PostTagDTO(BaseModel):
    tag_id: UUID
    name: str
