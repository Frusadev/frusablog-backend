from datetime import datetime
from typing import Optional, get_args
from uuid import UUID, uuid4

from pydantic import field_validator
from sqlmodel import Field, Relationship, Session, SQLModel

from app.dto.comment_dto import CommentDTO
from app.dto.media_dto import ContentTypeLiteral, MediaDTO
from app.dto.notification_dto import NotificationDTO
from app.dto.post_dto import PostDTO
from app.dto.posttag_dto import PostTagDTO
from app.dto.user_dto import UserDTO
from app.utils.crypto import gen_id


class PostTagLink(SQLModel, table=True):
    post_id: UUID = Field(foreign_key="post.post_id", primary_key=True)
    tag_id: UUID = Field(foreign_key="posttag.tag_id", primary_key=True)


class UserPostLikeLink(SQLModel, table=True):
    post_id: UUID = Field(foreign_key="post.post_id", primary_key=True)
    username: str = Field(foreign_key="user.username", primary_key=True)


class UserCommentLikeLink(SQLModel, table=True):
    comment_id: UUID = Field(
        foreign_key="comment.comment_id", primary_key=True
    )
    username: str = Field(foreign_key="user.username", primary_key=True)


class User(SQLModel, table=True):
    username: str = Field(primary_key=True)
    role_id: str = Field(foreign_key="role.role_id", unique=True)
    avatar_url: Optional[str]
    display_name: str
    email: str
    hashed_password: str
    last_login: datetime
    bio: Optional[str]
    work_industry: Optional[str]
    location: Optional[str]
    work_title: Optional[str]
    account_verified: bool = False
    poster: bool = False
    in_newsletter: bool = False
    role: "Role" = Relationship(back_populates="users")
    posts: list["Post"] = Relationship(
        back_populates="author", cascade_delete=True
    )
    comments: list["Comment"] = Relationship(
        back_populates="author", cascade_delete=True
    )
    liked_posts: list["Post"] = Relationship(
        back_populates="liked_by",
        link_model=UserPostLikeLink,
    )
    liked_comments: list["Comment"] = Relationship(
        back_populates="liked_by",
        link_model=UserCommentLikeLink,
    )
    login_sessions: list["LoginSession"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    auth_sessions: list["AuthSession"] = Relationship(
        back_populates="user", cascade_delete=True
    )
    medias: list["Media"] = Relationship(
        back_populates="uploader", cascade_delete=True
    )
    notifications: list["Notification"] = Relationship(
        back_populates="user", cascade_delete=True
    )

    def update_from_dto(
        self, dto: UserDTO, db_session: Session, commit: bool = True
    ):
        self.display_name = dto.display_name
        self.avatar_url = dto.avatar_url
        self.last_login = dto.last_login
        self.bio = dto.bio
        self.work_industry = dto.work_industry
        self.location = dto.location
        self.work_title = dto.work_title

        if commit:
            db_session.add(self)
            db_session.commit()

    def to_dto(self) -> UserDTO:
        return UserDTO(
            username=self.username,
            display_name=self.display_name,
            role_id=self.role_id,
            avatar_url=self.avatar_url,
            last_login=self.last_login,
            bio=self.bio,
            work_industry=self.work_industry,
            location=self.location,
            work_title=self.work_title,
            poster=self.poster,
        )


class Role(SQLModel, table=True):
    role_id: str = Field(default_factory=gen_id, primary_key=True)
    role_type: str  # admin, moderator, user
    permissions: list["Permission"] = Relationship(back_populates="role")
    users: User = Relationship(back_populates="role")


class Permission(SQLModel, table=True):
    permission_id: str = Field(default_factory=gen_id, primary_key=True)
    name: str = Field(primary_key=True)
    role_id: str = Field(foreign_key="role.role_id")
    role: Role = Relationship(back_populates="permissions")


class Media(SQLModel, table=True):
    media_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    protected: bool = False
    media_type: str
    description: str
    uploader_username: str = Field(foreign_key="user.username")
    uploader: User = Relationship(back_populates="medias")

    @field_validator("media_type")
    def validate_media_type(cls, value: str):
        if value not in get_args(ContentTypeLiteral):
            raise ValueError(
                f"Invalid media type: {value}. Must be one of {get_args(ContentTypeLiteral)}"
            )

    def to_dto(self) -> MediaDTO:
        return MediaDTO(
            media_id=self.media_id,
            name=self.name,
            protected=self.protected,
            description=self.description,
            content_type=self.media_type,
        )


class PostMedia(SQLModel, table=True):
    media_id: UUID = Field(foreign_key="media.media_id", primary_key=True)
    post_id: UUID = Field(foreign_key="post.post_id")
    cover_image: bool = False  # If false, will be considered as an attachment.
    post: "Post" = Relationship(back_populates="medias")
    media: Media = Relationship()

    def to_dto(self) -> MediaDTO:
        return MediaDTO(
            media_id=self.media_id,
            name=self.media.name,
            protected=self.media.protected,
            description=self.media.description,
            content_type=self.media.media_type,
        )


class Notification(SQLModel, table=True):
    notification_id: UUID = Field(default_factory=uuid4, primary_key=True)
    username: str = Field(foreign_key="user.username")
    content: str
    action: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    read: bool = False
    user: User = Relationship(back_populates="notifications")

    def to_dto(self) -> NotificationDTO:
        return NotificationDTO(
            id=self.notification_id,
            content=self.content,
            username=self.username,
            viewed=self.read,
        )

    def update_from_dto(
        self, dto: NotificationDTO, db_session: Session, commit: bool = True
    ):
        self.content = dto.content
        self.read = dto.viewed

        if commit:
            db_session.add(self)
            db_session.commit()


class Post(SQLModel, table=True):
    post_id: UUID = Field(default_factory=uuid4, primary_key=True)
    author_username: str = Field(foreign_key="user.username")
    created_at: datetime
    last_modified: datetime
    modified: bool = False
    featured: bool = False
    title: str
    description: str
    content: str
    published: bool = False
    medias: list[PostMedia] = Relationship(back_populates="post")
    author: User = Relationship(back_populates="posts")
    liked_by: list[User] = Relationship(
        back_populates="liked_posts", link_model=UserPostLikeLink
    )
    comments: list["Comment"] = Relationship(
        back_populates="post", cascade_delete=True
    )
    tags: list["PostTag"] = Relationship(
        back_populates="posts", link_model=PostTagLink
    )

    def get_likes_count(self):
        return len(self.liked_by)

    def get_comments_count(self):
        return len(self.comments)

    def to_dto(self) -> PostDTO:
        return PostDTO(
            post_id=self.post_id,
            author_username=self.author_username,
            created_at=self.created_at,
            last_modified=self.last_modified,
            modified=self.modified,
            title=self.title,
            description=self.description,
            content=self.content,
            published=self.published,
            like_count=self.get_likes_count(),
            comments_count=self.get_comments_count(),
            tags=[tag.to_dto() for tag in self.tags],
            medias=[media.to_dto() for media in self.medias],
        )


class PostTag(SQLModel, table=True):
    tag_id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str
    posts: list[Post] = Relationship(
        back_populates="tags", link_model=PostTagLink
    )

    def to_dto(self) -> PostTagDTO:
        return PostTagDTO(
            tag_id=self.tag_id,
            name=self.name,
        )


class Comment(SQLModel, table=True):
    comment_id: UUID = Field(default_factory=uuid4, primary_key=True)
    post_id: UUID = Field(foreign_key="post.post_id")
    author_username: str = Field(foreign_key="user.username")
    created_at: datetime
    last_modified: datetime
    modified: bool = False
    content: str
    post: Post = Relationship(back_populates="comments")
    author: User = Relationship(back_populates="comments")
    liked_by: list[User] = Relationship(
        back_populates="liked_comments", link_model=UserCommentLikeLink
    )

    def get_likes_count(self):
        return len(self.liked_by)

    def to_dto(self) -> CommentDTO:
        return CommentDTO(
            comment_id=self.comment_id,
            post_id=self.post_id,
            author_username=self.author_username,
            created_at=self.created_at,
            last_modified=self.last_modified,
            modified=self.modified,
            content=self.content,
            likes_count=self.get_likes_count(),
        )


class WhiteListedEmail(SQLModel, table=True):
    email: str = Field(primary_key=True)


# This is a session model for storing user sessions
class LoginSession(SQLModel, table=True):
    session_id: str = Field(default_factory=gen_id, primary_key=True)
    username: str = Field(foreign_key="user.username")
    issued_at: datetime
    expires_at: datetime
    user: User = Relationship(back_populates="login_sessions")


# This is a session for authentication purposes.
class AuthSession(SQLModel, table=True):
    session_id: str = Field(default_factory=gen_id, primary_key=True)
    username: str = Field(foreign_key="user.username")
    issued_at: datetime
    expires_at: datetime
    user: User = Relationship(back_populates="auth_sessions")
