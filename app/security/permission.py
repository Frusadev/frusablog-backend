from typing import Literal, Optional

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from app.db.models import Permission, Role

POST_RESOURCE = "post"
COMMENT_RESOURCE = "comment"
USER_RESOURCE = "user"
MEDIA_RESOURCE = "media"
TAG_RESOURCE = "tag"

ACTION_CREATE = "create"
ACTION_READ = "read"
ACTION_UPDATE = "update"
ACTION_DELETE = "delete"
ACTION_CRUD = "crud"
ADMIN_ACTION = "admin_action"


def create_global_permission(
    role_id: str,
    db_session: Session,
    resource_name: str,
    action_name: str,
    commit: bool = True,
):
    role = db_session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Role not found."
        )
    permission_in_db = db_session.exec(
        select(Permission).where(
            Permission.role_id == role_id,
            Permission.name == f"{resource_name}:{action_name}",
        )
    ).first()
    if permission_in_db:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user already has this permission.",
        )
    permission = Permission(
        name=f"{resource_name}:{action_name}",
        role_id=role_id,
    )
    if commit:
        db_session.add(permission)
        db_session.commit()
        db_session.refresh(permission)
    else:
        db_session.add(permission)
        return permission


def create_permission(
    role_id: str,
    db_session: Session,
    resource_name: str,
    resource_id: str,
    action_name: str,
    commit: bool = True,
):
    role = db_session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Role not found."
        )
    permission_in_db = db_session.exec(
        select(Permission).where(
            Permission.role_id == role_id,
            Permission.name == f"{resource_name}:{resource_id}:{action_name}",
        )
    ).first()
    if permission_in_db:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail="The user already has this permission.",
        )
    permission = Permission(
        name=f"{resource_name}:{resource_id}:{action_name}",
        role_id=role_id,
    )
    if commit:
        db_session.add(permission)
        db_session.commit()
        db_session.refresh(permission)
    else:
        db_session.add(permission)
        return permission


def has_permission(
    db_session: Session,
    role_id: str,
    bypass_role: Optional[Literal["admin", "user", "moderator"]],
    resource_name: str,
    resource_id: str,
    action_name: str,
) -> bool:
    role = db_session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Role not found."
        )
    if role.role_type == bypass_role:
        return True

    permission = db_session.exec(
        select(Permission).where(
            Permission.role_id == role_id,
            Permission.name == f"{resource_name}:{resource_id}:{action_name}",
        )
    ).first()
    return permission is not None


def has_crud_permission(
    db_session: Session,
    role_id: str,
    bypass_role: Optional[Literal["admin", "user", "moderator"]],
    resource_name: str,
    resource_id: str,
) -> bool:
    return has_permission(
        db_session=db_session,
        role_id=role_id,
        bypass_role=bypass_role,
        resource_name=resource_name,
        resource_id=resource_id,
        action_name=ACTION_CRUD,
    )


def has_global_permission(
    db_session: Session,
    role_id: str,
    bypass_role: Optional[
        Literal["admin", "user", "moderator"]
    ],  # Required role type (admin, user, moderator)
    resource_name: str,
    action_name: str,
) -> bool:
    role = db_session.get(Role, role_id)
    if not role:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Role not found."
        )
    if role.role_type == bypass_role:
        return True

    permission = db_session.exec(
        select(Permission).where(
            Permission.role_id == role_id,
            Permission.name == f"{resource_name}:{action_name}",
        )
    ).first()
    return permission is not None


def has_global_crud_permission(
    db_session: Session,
    role_id: str,
    bypass_role: Optional[Literal["admin", "user", "moderator"]],
    resource_name: str,
) -> bool:
    return has_global_permission(
        db_session=db_session,
        role_id=role_id,
        bypass_role=bypass_role,
        resource_name=resource_name,
        action_name=ACTION_CRUD,
    )
