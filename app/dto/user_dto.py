from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserDTO(BaseModel):
    username: str
    display_name: str
    role_id: str
    avatar_url: Optional[str]
    last_login: datetime
    bio: Optional[str]
    work_industry: Optional[str]
    location: Optional[str]
    work_title: Optional[str]
    post_count: Optional[int] = None
    poster: bool
