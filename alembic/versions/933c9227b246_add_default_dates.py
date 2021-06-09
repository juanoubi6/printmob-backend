"""add_default_dates

Revision ID: 933c9227b246
Revises: f8a55994f37c
Create Date: 2021-06-06 09:19:45.512755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import func

revision = '933c9227b246'
down_revision = 'f8a55994f37c'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('campaign', sa.Column('created_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('campaign', sa.Column('updated_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('campaign', sa.Column('deleted_at', sa.DateTime, nullable=True))
    op.add_column('users', sa.Column('created_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('users', sa.Column('updated_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('users', sa.Column('deleted_at', sa.DateTime, nullable=True))
    op.drop_column('pledges', 'pledge_date')
    op.add_column('pledges', sa.Column('created_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('pledges', sa.Column('updated_at', sa.DateTime, server_default=func.now(), nullable=False))
    op.add_column('pledges', sa.Column('deleted_at', sa.DateTime, nullable=True))


def downgrade():
    op.drop_column('campaign', 'created_at')
    op.drop_column('campaign', 'updated_at')
    op.drop_column('campaign', 'deleted_at')
    op.drop_column('users', 'created_at')
    op.drop_column('users', 'updated_at')
    op.drop_column('users', 'deleted_at')
    op.drop_column('pledges', 'created_at')
    op.drop_column('pledges', 'updated_at')
    op.drop_column('pledges', 'deleted_at')
    op.add_column('pledges', sa.Column('pledge_date', sa.DateTime, nullable=False))
