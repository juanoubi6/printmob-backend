"""close_campaign_model_changes

Revision ID: bb2106410b34
Revises: 68b4e2cd5c4b
Create Date: 2021-06-19 14:43:02.092474

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bb2106410b34'
down_revision = '68b4e2cd5c4b'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('campaign', sa.Column('status', sa.String(30), nullable=False))


def downgrade():
    op.drop_column('campaign', 'status')
