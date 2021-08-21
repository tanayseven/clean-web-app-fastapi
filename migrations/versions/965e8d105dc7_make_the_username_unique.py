"""make the username unique

Revision ID: 965e8d105dc7
Revises: 7de037f185ea
Create Date: 2021-08-09 23:30:43.601731

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "965e8d105dc7"
down_revision = "7de037f185ea"
branch_labels = None
depends_on = None


def upgrade():
    op.create_unique_constraint("unique_username", "user", ["username"])


def downgrade():
    op.drop_constraint("unique_username", "user", type_="unique")
