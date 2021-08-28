"""create blog

Revision ID: 5cacbc8d939c
Revises: 965e8d105dc7
Create Date: 2021-08-28 12:22:48.028151

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5cacbc8d939c'
down_revision = '965e8d105dc7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('blog_post',
        sa.Column('id', postgresql.UUID(), nullable=False),
        sa.Column('content', sa.Text(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('blog_post')
