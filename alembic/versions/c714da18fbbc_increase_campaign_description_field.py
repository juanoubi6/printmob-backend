"""increase_campaign_description_field

Revision ID: c714da18fbbc
Revises: 2ee06a00e2ca
Create Date: 2021-08-19 09:13:57.564654

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c714da18fbbc'
down_revision = '2ee06a00e2ca'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('campaign', 'description', type_=sa.String, existing_type=sa.TEXT)


def downgrade():
    op.alter_column('campaign', 'description', type_=sa.TEXT, existing_type=sa.String)
