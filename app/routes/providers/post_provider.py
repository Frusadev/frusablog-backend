from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session, select
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.db.models import Media, Post, PostMedia, PostTag, User
from app.dto.post_dto import PostCreateDTO, PostUpdateDTO
from app.security.permission import (
    ACTION_CRUD,
    ACTION_UPDATE,
    POST_RESOURCE,
    create_permission,
    has_crud_permission,
    has_permission,
)


async def get_posts(
    db_session: Session,
    skip: int = 0,
    limit: int = 10,
    tags: Optional[List[str]] = None,
    author: Optional[str] = None,
    published_only: bool = True,
):
    """Get all posts with optional filtering"""
    query = select(Post)

    if published_only:
        query = query.where(Post.published)

    if tags:
        query = query.join(PostTag).where(PostTag.name in tags)

    if author:
        query = query.where(Post.author_username == author)

    posts = db_session.exec(query.offset(skip).limit(limit)).all()
    return [post.to_dto() for post in posts]


async def get_post(
    db_session: Session,
    post_id: UUID,
    current_user: Optional[User] = None,
):
    """Get a specific post by ID"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found."
        )

    # If post is not published, only the author can view it
    if not post.published and (
        not current_user or current_user.username != post.author_username
    ):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Post not available."
        )

    return post


async def create_post(
    db_session: Session,
    post_data: PostCreateDTO,
    current_user: User,
):
    """Create a new post"""
    now = datetime.utcnow()
    post = Post(
        author_username=current_user.username,
        created_at=now,
        last_modified=now,
        title=post_data.title,
        description=post_data.description,
        content=post_data.content,
        published=post_data.published,
    )

    # Add tags if provided
    if post_data.tags:
        for tag_name in post_data.tags:
            # Check if tag exists, create if not
            tag_query = select(PostTag).where(PostTag.name == tag_name)
            tag = db_session.exec(tag_query).first()
            if not tag:
                tag = PostTag(name=tag_name)
                db_session.add(tag)
                db_session.commit()
                db_session.refresh(tag)
            post.tags.append(tag)

    permission = create_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        action_name=ACTION_CRUD,
    )

    db_session.add(post)
    db_session.add(permission)
    db_session.commit()
    db_session.refresh(post)
    return post.to_dto()


async def update_post(
    db_session: Session,
    post_id: UUID,
    post_data: PostUpdateDTO,
    current_user: User,
):
    """Update an existing post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Only the author can update the post
    if not has_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        action_name=ACTION_UPDATE,
        bypass_role=None,
    ) or has_crud_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    # Update post fields
    if post_data.title is not None:
        post.title = post_data.title
    if post_data.description is not None:
        post.description = post_data.description
    if post_data.content is not None:
        post.content = post_data.content
    if post_data.published is not None:
        post.published = post_data.published

    post.last_modified = datetime.utcnow()
    post.modified = True

    # Update tags if provided
    if post_data.tags is not None:
        # Clear existing tags
        post.tags = []

        # Add new tags
        for tag_name in post_data.tags:
            tag_query = select(PostTag).where(PostTag.name == tag_name)
            tag = db_session.exec(tag_query).first()
            if not tag:
                tag = PostTag(name=tag_name)
                db_session.add(tag)
                db_session.commit()
                db_session.refresh(tag)
            post.tags.append(tag)

    db_session.add(post)
    db_session.commit()
    db_session.refresh(post)
    return post.to_dto()


async def delete_post(
    db_session: Session,
    post_id: UUID,
    current_user: User,
):
    """Delete a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Only the author can delete the post
    if not has_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        action_name=ACTION_CRUD,
        bypass_role="admin",
    ) or has_crud_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        bypass_role="admin",
    ):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )

    db_session.delete(post)
    db_session.commit()
    return {"message": "Post deleted successfully"}


async def like_post(
    db_session: Session,
    post_id: UUID,
    current_user: User,
):
    """Like a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user already liked the post
    if current_user in post.liked_by:
        return {"message": "Post already liked"}

    post.liked_by.append(current_user)
    db_session.commit()
    return post.get_likes_count()


async def has_liked_post(
    db_session: Session,
    post_id: UUID,
    current_user: User,
):
    """Check if the user has liked a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user liked the post
    return current_user in post.liked_by


async def unlike_post(
    db_session: Session,
    post_id: UUID,
    current_user: User,
):
    """Unlike a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Check if user liked the post
    if current_user not in post.liked_by:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="User has not liked this post.",
        )

    post.liked_by.remove(current_user)
    db_session.commit()
    return post.get_likes_count()


async def add_media_to_post(
    db_session: Session,
    post_id: UUID,
    media_id: UUID,
    description: str,
    is_cover: bool,
    current_user: User,
):
    """Add media to a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Only the author can add media to the post
    if not has_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        action_name=ACTION_UPDATE,
        bypass_role=None,
    ) or has_crud_permission(
        db_session=db_session,
        role_id=current_user.role_id,
        resource_name=POST_RESOURCE,
        resource_id=str(post.post_id),
        bypass_role=None,
    ):
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    # Check if media exists
    media = db_session.get(Media, media_id)
    if not media:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Media not found"
        )

    # Create post media link
    post_media = PostMedia(
        media_id=media_id,
        post_id=post_id,
        cover_image=is_cover,
    )

    # If this is a cover image, set all other media for this post to not be covers
    if is_cover:
        existing_covers = db_session.exec(
            select(PostMedia)
            .where(PostMedia.post_id == post_id)
            .where(PostMedia.cover_image == True)
        ).all()
        for cover in existing_covers:
            cover.cover_image = False
            db_session.add(cover)

    db_session.add(post_media)
    db_session.commit()
    db_session.refresh(post_media)

    return post.to_dto()


async def remove_media_from_post(
    db_session: Session,
    post_id: UUID,
    media_id: UUID,
    current_user: User,
):
    """Remove media from a post"""
    post = db_session.get(Post, post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    # Only the author can remove media from the post
    if post.author_username != current_user.username:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )

    # Find post media link
    post_media = db_session.exec(
        select(PostMedia)
        .where(PostMedia.post_id == post_id)
        .where(PostMedia.media_id == media_id)
    ).first()

    if not post_media:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail="Media not attached to this post",
        )

    db_session.delete(post_media)
    db_session.commit()

    return post.to_dto()
