from pydantic import BaseModel

from app.models.Models import CommentModel


class Comment(BaseModel):
    comment_id: int | None = None
    post_id: int
    user_id: int
    comment_content: str
    likes: int = 0
    date: int
    edited: bool = False
    parent_comment_id: int | None = None

    def inc_likes(self):
        self.likes += 1

    def to_comment_model(self) -> CommentModel:
        model = CommentModel(
            user_id=self.user_id,
            post_id=self.post_id,
            likes=self.likes,
            date=self.date,
            comment_content=self.comment_content,
            edited=self.edited
        )

        if self.comment_id:
            model.comment_id = self.comment_id

        if self.parent_comment_id:
            model.parent_comment_id = self.parent_comment_id

        return model

    def create_comment(self, model: CommentModel):
        self.comment_id = model.comment_id
        self.post_id = model.post_id
        self.user_id = model.user_id
        self.likes = model.likes
        self.date = model.date
        self.edited = model.edited
        self.comment_content = model.comment_content
        self.parent_comment_id = model.parent_comment_id
