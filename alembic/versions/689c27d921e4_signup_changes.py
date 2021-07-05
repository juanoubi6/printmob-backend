"""signup changes

Revision ID: 689c27d921e4
Revises: d2bb987591c1
Create Date: 2021-07-05 14:47:07.019466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689c27d921e4'
down_revision = 'd2bb987591c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        index_name='unique_username_idx',
        table_name='users',
        columns=['user_name'],
        unique=True
    )


def downgrade():
    op.drop_index("unique_username_idx")
