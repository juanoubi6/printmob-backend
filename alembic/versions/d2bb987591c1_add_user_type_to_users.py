"""add_user_type_to_users

Revision ID: d2bb987591c1
Revises: 4214f8990ffc
Create Date: 2021-07-03 20:09:16.635721

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2bb987591c1'
down_revision = '4214f8990ffc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('type', sa.String(30), nullable=False))


def downgrade():
    op.drop_column('users', 'type')
