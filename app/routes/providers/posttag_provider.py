from sqlmodel import Session, select

from app.db.models import Post, PostTag


async def get_tags(
    db_session: Session,
    skip: int = 0,
    limit: int = 100,
):
    """Get all post tags"""
    tags = db_session.exec(select(PostTag).offset(skip).limit(limit)).all()
    return [tag.to_dto() for tag in tags]


async def get_posts_by_tag(
    db_session: Session,
    tag_name: str,
    skip: int = 0,
    limit: int = 10,
    published_only: bool = True,
):
    """Get all posts with a specific tag"""
    query = select(Post).join(PostTag).where(PostTag.name == tag_name)

    if published_only:
        query = query.where(Post.published)

    posts = db_session.exec(query.offset(skip).limit(limit)).all()
    return posts
