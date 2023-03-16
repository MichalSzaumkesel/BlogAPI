"""add foreign key to posts table

Revision ID: be98f2bfe422
Revises: f75dabaa27d0
Create Date: 2023-03-15 15:37:47.739651

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be98f2bfe422'
down_revision = 'f75dabaa27d0'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('author_id', sa.Integer, nullable=False))
    op.create_foreign_key('posts_users_fkey', source_table='posts', referent_table='users',
                          local_cols=['author_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'author_id')
    pass
