from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND

from app.db.models import Notification


async def get_notifications(
    db_session: Session, skip: int, limit: int, unread_only: bool = True
):
    stmt = (
        select(Notification)
        .where(Notification.read == (not unread_only))
        .offset(skip)
        .limit(limit)
    )
    notifications = db_session.exec(stmt)
    return [notif.to_dto() for notif in notifications]


async def get_notification(db_session: Session, notification_id: UUID):
    notification = db_session.get(Notification, notification_id)
    if not notification:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Notification not found"
        )
    return notification.to_dto()
