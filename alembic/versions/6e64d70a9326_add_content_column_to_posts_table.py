"""add content column to posts table

Revision ID: 6e64d70a9326
Revises: bfb26b9cf407
Create Date: 2023-03-15 15:14:58.035741

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6e64d70a9326'
down_revision = 'bfb26b9cf407'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String, nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
