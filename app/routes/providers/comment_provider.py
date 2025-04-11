from datetime import datetime
from uuid import UUID

from fastapi import HTTPException
from sqlmodel import Session
from starlette.status import HTTP_403_FORBIDDEN, HTTP_404_NOT_FOUND

from app.db.models import Comment, Post, User
from app.dto.comment_dto import CommentCreateDTO, CommentUpdateDTO


async def get_comment(
    db_session: Session,
    comment_id: UUID,
):
    """Get a specific comment by ID"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )
    return comment.to_dto()


async def create_comment(
    db_session: Session,
    comment_data: CommentCreateDTO,
    current_user: User,
):
    """Create a new comment on a post"""
    # Check if post exists
    post = db_session.get(Post, comment_data.post_id)
    if not post:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Post not found"
        )

    now = datetime.utcnow()
    comment = Comment(
        post_id=comment_data.post_id,
        author_username=current_user.username,
        created_at=now,
        last_modified=now,
        content=comment_data.content,
    )
    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment


async def update_comment(
    db_session: Session,
    comment_id: UUID,
    comment_data: CommentUpdateDTO,
    current_user: User,
):
    """Update an existing comment"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Only the author can update the comment
    if comment.author_username != current_user.username:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to update this comment",
        )

    comment.content = comment_data.content
    comment.last_modified = datetime.utcnow()
    comment.modified = True

    db_session.add(comment)
    db_session.commit()
    db_session.refresh(comment)
    return comment.to_dto()


async def delete_comment(
    db_session: Session,
    comment_id: UUID,
    current_user: User,
):
    """Delete a comment"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Only the author can delete the comment
    if comment.author_username != current_user.username:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment",
        )

    db_session.delete(comment)
    db_session.commit()
    return {"message": "Comment deleted successfully"}


async def like_comment(
    db_session: Session,
    comment_id: UUID,
    current_user: User,
):
    """Like a comment"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Check if user already liked the comment
    if current_user in comment.liked_by:
        return {"message": "Comment already liked"}

    comment.liked_by.append(current_user)
    db_session.commit()
    return {
        "message": "Comment liked successfully",
        "likes_count": len(comment.liked_by),
    }


async def unlike_comment(
    db_session: Session,
    comment_id: UUID,
    current_user: User,
):
    """Unlike a comment"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    # Check if user liked the comment
    if current_user not in comment.liked_by:
        return {"message": "Comment not liked yet"}

    comment.liked_by.remove(current_user)
    db_session.commit()
    return {
        "message": "Comment unliked successfully",
        "likes_count": len(comment.liked_by),
    }


async def has_user_liked_comment(
    db_session: Session,
    comment_id: UUID,
    current_user: User,
):
    """Check if the user has liked the comment"""
    comment = db_session.get(Comment, comment_id)
    if not comment:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND, detail="Comment not found"
        )

    return current_user in comment.liked_by
