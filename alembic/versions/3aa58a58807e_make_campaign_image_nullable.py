"""make_campaign_image_nullable

Revision ID: 3aa58a58807e
Revises: 933c9227b246
Create Date: 2021-06-08 23:39:52.114634

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3aa58a58807e'
down_revision = '933c9227b246'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('campaign', 'campaign_picture_url', nullable=True)


def downgrade():
    op.alter_column('campaign', 'campaign_picture_url', nullable=False)
