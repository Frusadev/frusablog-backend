from pydantic import BaseModel

from app.models.Models import PostModel
from app.schemas.Comment import Comment


class Post(BaseModel):
    post_id: int | None = None
    user_id: int
    post_title: str
    post_content: str
    likes: int = 0
    date: int
    edited: bool = False
    comments: list[Comment] | None = None

    def inc_likes(self):
        self.likes += 1

    def to_post_model(self) -> PostModel:
        model = PostModel(
            post_title=self.post_title,
            post_content=self.post_content,
            user_id=self.user_id,
            likes=self.likes,
            date=self.date,
            edited=self.edited,
        )
        if self.comments:
            model_comments = list(
                map(lambda comment: comment.to_comment_model(), self.comments)
            )
            model.comments = model_comments

        if self.post_id:
            model.post_id = self.post_id
        return model

    def create_post(self, model: PostModel):
        self.post_id = model.post_id
        self.user_id = model.user_id
        self.post_content = model.post_content
        self.post_title = model.post_title
        self.date = model.date
        self.edited = model.edited
        comments: list[Comment] = []

        for comment_model in model.comments:
            comment: Comment = Comment(
                comment_id=0, post_id=0, user_id=0, comment_content="", date=0
            )
            comment.create_comment(comment_model)
            comments.append(comment)

        if comments:
            self.comments = comments
