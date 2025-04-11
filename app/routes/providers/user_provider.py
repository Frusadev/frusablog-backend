from typing import Literal

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND,
)

from app.db.models import Post, User, WhiteListedEmail
from app.dto.user_dto import UserDTO
from app.security.permission import (
    ACTION_CRUD,
    ADMIN_ACTION,
    USER_RESOURCE,
    has_permission,
)


async def get_user_posts(
    db_session: Session,
    current_user: User,
    username: str,
    skip: int = 0,
    limit: int = 10,
    published_only: bool = True,
):
    """Get all posts by a specific user"""
    query = select(Post).where(Post.author_username == username)

    # If requesting user is not the author, only show published posts
    if published_only and (
        has_permission(
            db_session=db_session,
            role_id=current_user.role_id,
            resource_name=USER_RESOURCE,
            resource_id=username,
            action_name=ACTION_CRUD,
            bypass_role="admin",
        )
    ):
        query = query.where(Post.published)

    posts = db_session.exec(query.offset(skip).limit(limit)).all()
    return posts


async def get_user_profile(
    db_session: Session,
    username: str,
):
    """Get a user's public profile"""
    user = db_session.get(User, username)
    if not user:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="User not found"
        )

    # Get post count
    post_count = len(user.posts)
    return UserDTO(
        username=user.username,
        display_name=user.display_name,
        avatar_url=user.avatar_url,
        bio=user.bio,
        work_industry=user.work_industry,
        work_title=user.work_title,
        location=user.location,
        role_id=user.role_id,
        last_login=user.last_login,
        post_count=post_count,
    )


async def get_user_email(db_session: Session, user: User):
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role="admin",
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )
    return user.email


WorkIndustries = Literal[
    "Software Engineering",
    "Data Science",
    "Design",
    "Marketing",
    "Sales",
    "Finance",
    "Healthcare",
    "Education",
    "Manufacturing",
    "Retail",
    "Hospitality",
    "Construction",
    "Transportation",
    "Legal",
    "Government",
]


async def change_work_industry(
    db_session: Session, user: User, industry: WorkIndustries
):
    """Change the work industry of a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    user.work_industry = industry
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.to_dto()


async def change_bio(db_session: Session, user: User, bio: str):
    """Change the bio of a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    user.bio = bio
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.to_dto()


async def change_location(db_session: Session, user: User, location: str):
    """Change the location of a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    user.location = location
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.to_dto()


async def change_work_title(db_session: Session, user: User, title: str):
    """Change the work title of a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    user.work_title = title
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user.to_dto()


async def unsubscribe(db_session: Session, user: User):
    """Unsubscribe a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    db_session.delete(user)
    db_session.commit()
    return {"detail": "User unsubscribed successfully."}


async def delete_user(
    db_session: Session,
    user: User,
    whitelist: bool = False,
):
    """Delete a role from a user"""
    if not has_permission(
        db_session=db_session,
        role_id=user.role_id,
        resource_name=USER_RESOURCE,
        resource_id=user.username,
        action_name=ACTION_CRUD,
        bypass_role="admin",
    ):
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Not authorized to access this resource",
        )

    if whitelist:
        if not has_permission(
            db_session=db_session,
            role_id=user.role_id,
            resource_name=USER_RESOURCE,
            resource_id=user.username,
            action_name=ADMIN_ACTION,
            bypass_role="admin",
        ):
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail="Not authorized to access this resource.",
            )
        db_session.add(WhiteListedEmail(email=user.email))

    db_session.delete(user)
    db_session.commit()
    return {"detail": "User deleted successfully."}


async def get_current_user(user: User):
    return user.to_dto()
