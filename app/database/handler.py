from sqlalchemy.orm import Session

from app.database.db import Base, engine
from app.database.errors import ElementNotFoundError
from app.models.Models import CommentModel, PostModel, UserModel
from app.schemas.Comment import Comment
from app.schemas.Post import Post
from app.schemas.User import User

Base.metadata.create_all(engine)

local_session = Session(engine)


def get_user_by_name(username: str) -> User:
    with local_session as session:
        user_model = (
            session.query(UserModel).where(UserModel.username == username).first()
        )
        if user_model:
            user = User(username="", name="", hashed_password="")
            user.create_user(user_model)
            return user
        raise ElementNotFoundError(f"Unable to find user: {username}")


def get_user(user_id: int) -> User:
    """Retrieve a user from the database by their ID.

    Args:
        user_id (int): The ID of the user to retrieve.

    Returns:
        User: An instance of the User schema populated with user data if found.
    """
    with local_session as session:
        user_model = session.get(UserModel, user_id)
        if user_model:
            user = User(username="", name="", hashed_password="")
            user.create_user(user_model)
            return user
        raise ElementNotFoundError(f"Unable to find user {user_id}")


# def get_user(user_id: int) -> User:
#     """Retrieve a user from the database by their ID.
#
#     Args:
#         user_id (int): The ID of the user to retrieve.
#
#     Returns:
#         User: An instance of the User schema populated with user data if found.
#         int: An error code indicating that the user was not found.
#     """
#     with local_session as session:
#         user_model = session.get(UserModel, user_id)
#         if user_model:
#             user = User(username="", hashed_password="")
#             user.create_user(user_model)
#             return user
#         else:
#             raise ElementNotFoundError(f"Unable to find user {user_id}")


def get_post(post_id: int) -> Post:
    """Retrieve a post from the database by its ID.

    Args:
        post_id (int): The ID of the post to retrieve.

    Returns:
        Post: An instance of the Post schema populated with post data if found.
    """
    with local_session as session:
        post_model = session.get(PostModel, post_id)
        if post_model:
            post = Post(post_title="", user_id=0, post_content="", date=0)
            post.create_post(post_model)
            return post
        else:
            raise ElementNotFoundError(f"Unable to find post {post_id}")


def get_comment(comment_id: int) -> Comment:
    """Retrieve a comment from the database by its ID.

    Args:
        comment_id (int): The ID of the comment to retrieve.

    Returns:
        Comment: An instance of the Comment schema populated with comment data if found.
    """
    with local_session as session:
        comment_model = session.get(CommentModel, comment_id)
        if comment_model:
            comment = Comment(comment_content="", post_id=0, user_id=0, date=0)
            comment.create_comment(comment_model)
            return comment
        else:
            raise ElementNotFoundError(f"Unable to find comment {comment_id}")


def get_all_users():
    """Retrieve all users from the database.

    Returns:
        list[User]: A list of all users.
    """
    with local_session as session:
        user_models = session.query(UserModel).all()
        users = [
            User(
                username=u.username, name="", hashed_password=u.hashed_password
            ).create_user(u)
            for u in user_models
        ]
        return users


def get_all_posts():
    """Retrieve all posts from the database.

    Returns:
        list[Post]: A list of all posts.
    """
    with local_session as session:
        post_models = session.query(PostModel).all()
        posts = [
            Post(
                post_title=p.post_title,
                post_content=p.post_content,
                user_id=p.user_id,
                date=p.date,
            ).create_post(p)
            for p in post_models
        ]
        return posts


def get_all_comments():
    """Retrieve all comments from the database.

    Returns:
        list[Comment]: A list of all comments.
    """
    with local_session as session:
        comment_models = session.query(CommentModel).all()
        comments = [
            Comment(
                comment_content=c.comment_content,
                post_id=c.post_id,
                user_id=c.user_id,
                date=c.date,
            ).create_comment(c)
            for c in comment_models
        ]
        return comments


def get_posts_by_user(user_id: int):
    """Retrieve all posts created by a specific user.

    Args:
        user_id (int): The ID of the user whose posts are to be retrieved.

    Returns:
        list[Post]: A list of posts created by the specified user.
    """
    with local_session as session:
        post_models = session.query(PostModel).filter_by(user_id=user_id).all()
        posts = [
            Post(
                post_title=p.post_title,
                post_content=p.post_content,
                user_id=p.user_id,
                date=p.date,
            ).create_post(p)
            for p in post_models
        ]
        return posts


def get_comments_by_post(post_id: int):
    """Retrieve all comments associated with a specific post.

    Args:
        post_id (int): The ID of the post whose comments are to be retrieved.

    Returns:
        list[Comment]: A list of comments for the specified post.
    """
    with local_session as session:
        comment_models = session.query(CommentModel).filter_by(post_id=post_id).all()
        comments = [
            Comment(
                comment_content=c.comment_content,
                post_id=c.post_id,
                user_id=c.user_id,
                date=c.date,
            ).create_comment(c)
            for c in comment_models
        ]
        return comments


def get_comments_by_user(user_id: int):
    """Retrieve all comments made by a specific user.

    Args:
        user_id (int): The ID of the user whose comments are to be retrieved.

    Returns:
        list[Comment]: A list of comments made by the specified user.
    """
    with local_session as session:
        comment_models = session.query(CommentModel).filter_by(user_id=user_id).all()
        comments = [
            Comment(
                comment_content=c.comment_content,
                post_id=c.post_id,
                user_id=c.user_id,
                date=c.date,
            ).create_comment(c)
            for c in comment_models
        ]
        return comments


def count_posts_by_user(user_id: int) -> int:
    """Count the number of posts created by a specific user.

    Args:
        user_id (int): The ID of the user whose post count is to be retrieved.

    Returns:
        int: The count of posts created by the specified user.
    """
    with local_session as session:
        post_count = session.query(PostModel).filter_by(user_id=user_id).count()
        return post_count


def count_comments_by_post(post_id: int) -> int:
    """Count the number of comments associated with a specific post.

    Args:
        post_id (int): The ID of the post whose comment count is to be retrieved.

    Returns:
        int: The count of comments associated with the specified post.
    """
    with local_session as session:
        comment_count = session.query(CommentModel).filter_by(post_id=post_id).count()
        return comment_count


def remove_posts_by_user(user_id: int):
    """Remove all posts created by a specific user from the database.

    Args:
        user_id (int): The ID of the user whose posts are to be removed.
    """
    with local_session as session:
        _ = session.query(PostModel).filter_by(user_id=user_id).delete()
        session.commit()


def remove_comments_by_post(post_id: int):
    """Remove all comments associated with a specific post from the database.

    Args:
        post_id (int): The ID of the post whose comments are to be removed.
    """
    with local_session as session:
        _ = session.query(CommentModel).filter_by(post_id=post_id).delete()
        session.commit()


def add_user(user: User):
    """Add a new user to the database.

    Args:
        user (User): An instance of the User schema to be added.
    """
    with local_session as session:
        if user:
            session.add(user.to_user_model())
            session.commit()


def add_post(user_id: int, post: Post):
    """Add a new post associated with a specific user.

    Args:
        user_id (int): The ID of the user creating the post.
        post (Post): An instance of the Post schema to be added.
    """
    with local_session as session:
        user = session.get(UserModel, user_id)
        if user:
            post_model = post.to_post_model()
            session.add(post_model)
            user.posts.append(post_model)
            session.add(post_model)
            session.commit()


def add_comment(user_id: int, post_id: int, comment: Comment):
    """Add a new comment to a specific post made by a specific user.

    Args:
        user_id (int): The ID of the user making the comment.
        post_id (int): The ID of the post to which the comment is being added.
        comment (Comment): An instance of the Comment schema to be added.
    """
    with local_session as session:
        user = session.get(UserModel, user_id)
        post = session.get(PostModel, post_id)
        comment_model = comment.to_comment_model()

        if user and post:
            post.comments.append(comment_model)
            session.add(comment_model)
            user.comments.append(comment_model)
            session.commit()


def edit_user(user_id: int, username: str | None = None, password: str | None = None):
    """Edit the username and/or password of a specific user.

    Args:
        user_id (int): The ID of the user to be edited.
        username (str | None): The new username or None to leave unchanged.
        password (str | None): The new password or None to leave unchanged.
    """
    with local_session as session:
        user = session.get(UserModel, user_id)
        if user:
            if username:
                user.username = username

            if password:
                user.hashed_password = password
            session.commit()
        else:
            raise ElementNotFoundError(f"Unable to find user: {user_id}")


def edit_post(post_id: int, content: str):
    """Edit the content of a specific post.

    Args:
        post_id (int): The ID of the post to be edited.
        content (str): The new content for the post.
    """
    with local_session as session:
        post = session.get(PostModel, post_id)
        if post:
            post.post_content = content
            session.commit()
        else:
            raise ElementNotFoundError(f"Unable to find post: {post_id}")


def edit_comment(comment_id: int, content: str):
    """Edit the content of a specific comment.

    Args:
        comment_id (int): The ID of the comment to be edited.
        content (str): The new content for the comment.
    """
    with local_session as session:
        comment = session.get(CommentModel, comment_id)
        if comment:
            comment.comment_content = content
            session.commit()
        else:
            raise ElementNotFoundError(f"Unable to find comment {comment_id}")


def remove_user(user_id: int):
    """Remove a specific user from the database.

    Args:
        user_id (int): The ID of the user to be removed.
    """
    with local_session as session:
        _ = session.query(UserModel).filter_by(id=user_id).delete()
        session.commit()


def remove_post(post_id: int):
    """Remove a specific post from the database.

    Args:
        post_id (int): The ID of the post to be removed.
    """
    with local_session as session:
        _ = session.query(PostModel).filter_by(id=post_id).delete()
        session.commit()


def remove_comment(comment_id: int):
    """Remove a specific comment from the database.

    Args:
        comment_id (int): The ID of the comment to be removed.
    """
    with local_session as session:
        _ = session.query(CommentModel).filter_by(id=comment_id).delete()
        session.commit()
