"""create campaign table

Revision ID: 21e4b01f8f97
Revises: 
Create Date: 2021-05-24 11:42:04.167230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21e4b01f8f97'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'campaign',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
    )


def downgrade():
    op.drop_table('campaign')
