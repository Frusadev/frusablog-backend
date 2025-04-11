from typing import Annotated, List

from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.db.setup import get_db_session
from app.dto.post_dto import PostDTO
from app.dto.posttag_dto import PostTagDTO
from app.routes.providers import posttag_provider

posttag_router = APIRouter()


@posttag_router.get("/tags", response_model=List[PostTagDTO])
async def get_tags(
    db_session: Annotated[Session, Depends(get_db_session)],
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
):
    """Get all post tags"""
    return await posttag_provider.get_tags(
        db_session=db_session,
        skip=skip,
        limit=limit,
    )


@posttag_router.get("/tags/{tag_name}/posts", response_model=List[PostDTO])
async def get_posts_by_tag(
    db_session: Annotated[Session, Depends(get_db_session)],
    tag_name: str,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    published_only: bool = True,
):
    """Get all posts with a specific tag"""
    return await posttag_provider.get_posts_by_tag(
        db_session=db_session,
        tag_name=tag_name,
        skip=skip,
        limit=limit,
        published_only=published_only,
    )
