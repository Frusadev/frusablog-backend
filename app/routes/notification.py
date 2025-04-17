from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.models import User
from app.db.setup import get_db_session
from app.routes.providers import notification_provider
from app.routes.providers.auth_provider import get_current_user

notification_router = APIRouter()


@notification_router.get("/notifications")
async def get_notification(
    db_session: Annotated[Session, Depends(get_db_session)],
    _user: Annotated[User, Depends(get_current_user)],
    offset: int = Query(ge=0),
    limit: int = Query(0, ge=1, le=100),
    unread_only: bool = True,
):
    return notification_provider.get_notifications(
        db_session=db_session,
        skip=offset,
        limit=limit,
        unread_only=unread_only,
    )


@notification_router.get("/notifications/{notification_id}")
async def get(
    db_session: Annotated[Session, Depends(get_db_session)],
    _user: Annotated[User, Depends(get_current_user)],
    notification_id: UUID,
):
    return notification_provider.get_notification(
        db_session=db_session, notification_id=notification_id
    )
