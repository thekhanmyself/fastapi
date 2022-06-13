"""add content column to posts table

Revision ID: 3db236149496
Revises: c6fcc0a0e29c
Create Date: 2022-06-12 16:15:01.388083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3db236149496'
down_revision = 'c6fcc0a0e29c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
