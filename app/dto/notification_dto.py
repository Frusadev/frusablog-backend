from uuid import UUID

from pydantic import BaseModel


class NotificationDTO(BaseModel):
    id: UUID
    content: str
    username: str
    viewed: bool
