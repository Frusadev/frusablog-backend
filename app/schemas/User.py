from pydantic import BaseModel

from app.models.Models import UserModel
from app.schemas.Comment import Comment
from app.schemas.Post import Post


class User(BaseModel):
    user_id: int | None = None
    username: str
    name: str
    hashed_password: str
    posts: list[Post] | None = None
    comments: list[Comment] | None = None
    disabled: bool = False

    def to_user_model(self) -> UserModel:
        model = UserModel(
            username=self.username,
            name=self.name,
            hashed_password=self.hashed_password,
            disabled=self.disabled
        )

        if self.posts:
            model_posts = list(map(lambda post: post.to_post_model(), self.posts))
            model.posts = model_posts

        if self.comments:
            model_comments = list(
                map(lambda comment: comment.to_comment_model(), self.comments)
            )
            model.comments = model_comments

        if self.user_id:
            model.user_id = self.user_id

        return model

    def create_user(self, model: UserModel):
        self.user_id = model.user_id
        self.name = model.name
        self.username = model.username
        self.hashed_password = model.hashed_password
        self.disabled = model.disabled
        posts: list[Post] = []
        comments: list[Comment] = []

        for post_model in model.posts:
            post: Post = Post(
                post_id=0, user_id=0, post_content="", post_title="", date=0
            )
            post.create_post(post_model)
            posts.append(post)

        for comment_model in model.comments:
            comment: Comment = Comment(
                comment_id=0, post_id=0, user_id=0, comment_content="", date=0
            )
            comment.create_comment(comment_model)
            comments.append(comment)

        if posts:
            self.posts = posts

        if comments:
            self.comments = comments
