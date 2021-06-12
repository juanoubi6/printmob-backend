"""add_file_name_field_to_campign_model_images

Revision ID: 68b4e2cd5c4b
Revises: 3aa58a58807e
Create Date: 2021-06-12 01:07:54.897658

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '68b4e2cd5c4b'
down_revision = '3aa58a58807e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('campaign_model_images', sa.Column('file_name', sa.String, nullable=False))


def downgrade():
    op.drop_column('campaign_model_images', 'file_name')
