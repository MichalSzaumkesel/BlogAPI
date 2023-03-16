"""add user table

Revision ID: f75dabaa27d0
Revises: 6e64d70a9326
Create Date: 2023-03-15 15:25:17.740497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f75dabaa27d0'
down_revision = '6e64d70a9326'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer, nullable=False, primary_key=True),
                    sa.Column('email', sa.String(120), nullable=False, unique=True),
                    sa.Column('password', sa.String(60), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
                    )
    pass


def downgrade() -> None:
    pass
