"""empty message

Revision ID: e6b84071984e
Revises: 256fdd0c0d0a
Create Date: 2025-04-11 17:21:49.575283

"""
from typing import Sequence, Union

import sqlmodel

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e6b84071984e'
down_revision: Union[str, None] = '256fdd0c0d0a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posttag',
    sa.Column('tag_id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_table('role',
    sa.Column('role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('role_id')
    )
    op.create_table('whitelistedemail',
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('permission',
    sa.Column('permission_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.PrimaryKeyConstraint('permission_id', 'name')
    )
    op.create_table('user',
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('role_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('avatar_url', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('display_name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('email', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('hashed_password', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('last_login', sa.DateTime(), nullable=False),
    sa.Column('bio', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('work_industry', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('location', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('work_title', sqlmodel.sql.sqltypes.AutoString(), nullable=True),
    sa.Column('account_verified', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.role_id'], ),
    sa.PrimaryKeyConstraint('username'),
    sa.UniqueConstraint('role_id')
    )
    op.create_table('authsession',
    sa.Column('session_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('issued_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('loginsession',
    sa.Column('session_id', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('issued_at', sa.DateTime(), nullable=False),
    sa.Column('expires_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('session_id')
    )
    op.create_table('media',
    sa.Column('media_id', sa.Uuid(), nullable=False),
    sa.Column('name', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('protected', sa.Boolean(), nullable=False),
    sa.Column('media_type', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('uploader_username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['uploader_username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('media_id')
    )
    op.create_table('post',
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('author_username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.Boolean(), nullable=False),
    sa.Column('title', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('published', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['author_username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('post_id')
    )
    op.create_table('comment',
    sa.Column('comment_id', sa.Uuid(), nullable=False),
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('author_username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('last_modified', sa.DateTime(), nullable=False),
    sa.Column('modified', sa.Boolean(), nullable=False),
    sa.Column('content', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['author_username'], ['user.username'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.PrimaryKeyConstraint('comment_id')
    )
    op.create_table('postmedia',
    sa.Column('media_id', sa.Uuid(), nullable=False),
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('cover_image', sa.Boolean(), nullable=False),
    sa.ForeignKeyConstraint(['media_id'], ['media.media_id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.PrimaryKeyConstraint('media_id')
    )
    op.create_table('posttaglink',
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('tag_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['tag_id'], ['posttag.tag_id'], ),
    sa.PrimaryKeyConstraint('post_id', 'tag_id')
    )
    op.create_table('userpostlikelink',
    sa.Column('post_id', sa.Uuid(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['post.post_id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('post_id', 'username')
    )
    op.create_table('usercommentlikelink',
    sa.Column('comment_id', sa.Uuid(), nullable=False),
    sa.Column('username', sqlmodel.sql.sqltypes.AutoString(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comment.comment_id'], ),
    sa.ForeignKeyConstraint(['username'], ['user.username'], ),
    sa.PrimaryKeyConstraint('comment_id', 'username')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('usercommentlikelink')
    op.drop_table('userpostlikelink')
    op.drop_table('posttaglink')
    op.drop_table('postmedia')
    op.drop_table('comment')
    op.drop_table('post')
    op.drop_table('media')
    op.drop_table('loginsession')
    op.drop_table('authsession')
    op.drop_table('user')
    op.drop_table('permission')
    op.drop_table('whitelistedemail')
    op.drop_table('role')
    op.drop_table('posttag')
    # ### end Alembic commands ###
