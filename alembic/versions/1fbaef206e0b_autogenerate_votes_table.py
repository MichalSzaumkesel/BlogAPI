"""autogenerate votes table

Revision ID: 1fbaef206e0b
Revises: fc0cc3ac4c89
Create Date: 2023-03-15 18:41:14.195057

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '1fbaef206e0b'
down_revision = 'fc0cc3ac4c89'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('votes',
                    sa.Column('post_id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.Integer(), nullable=False),
                    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('post_id', 'user_id')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('votes')
    # ### end Alembic commands ###
