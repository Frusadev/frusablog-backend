from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class UserModel(Base):
    __tablename__: str = "users"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    name: Mapped[str]
    hashed_password: Mapped[str]
    posts: Mapped[list["PostModel"]] = relationship(
        "PostModel", cascade="all, delete-orphan", backref="post"
    )
    comments: Mapped[list["CommentModel"]] = relationship(
        "CommentModel", cascade="all, delete-orphan", backref="post"
    )
    disabled: Mapped[bool]

    def __init__(
        self, username: str, name: str, hashed_password: str, disabled: bool = False
    ):
        super().__init__()
        self.username = username
        self.name = name
        self.hashed_password = hashed_password
        self.disabled = disabled


class PostModel(Base):
    __tablename__: str = "posts"
    post_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    post_title: Mapped[str]
    post_content: Mapped[str]
    likes: Mapped[int]
    date: Mapped[int]
    edited: Mapped[bool]
    comments: Mapped[list["CommentModel"]] = relationship(
        "CommentModel", cascade="all, delete-orphan", backref="comment"
    )

    def __init__(
        self,
        post_content: str,
        user_id: int,
        post_title: str,
        likes: int,
        date: int,
        edited: bool = False,
    ):
        super().__init__()
        self.user_id = user_id
        self.post_content = post_content
        self.likes = likes
        self.post_title = post_title
        self.date = date
        self.edited = edited


class CommentModel(Base):
    __tablename__: str = "comments"
    comment_id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.post_id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
    comment_content: Mapped[str]
    likes: Mapped[int]
    date: Mapped[int]
    edited: Mapped[bool]
    parent_comment_id: Mapped[int] = mapped_column(
        ForeignKey("comments.comment_id"), nullable=True
    )

    def __init__(
        self,
        user_id: int,
        post_id: int,
        comment_content: str,
        likes: int,
        date: int,
        edited: bool = False,
    ):
        super().__init__()
        self.user_id = user_id
        self.post_id = post_id
        self.likes = likes
        self.date = date
        self.edited = edited
        self.comment_content = comment_content
