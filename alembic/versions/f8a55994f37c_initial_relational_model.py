"""Initial relational model

Revision ID: f8a55994f37c
Revises: 21e4b01f8f97
Create Date: 2021-05-30 14:44:10.683171

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = 'f8a55994f37c'
down_revision = '21e4b01f8f97'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=False),
        sa.Column('user_name', sa.String(255), nullable=False),
        sa.Column('date_of_birth', sa.DateTime, nullable=False),
        sa.Column('email', sa.String(255), nullable=False)
    )

    op.create_table(
        'printers',
        sa.Column('id', sa.Integer, primary_key=True)
    )

    op.create_foreign_key(
        'fk_printer_user',
        'printers', 'users',
        ['id'], ['id']
    )

    op.create_table(
        'buyers',
        sa.Column('id', sa.Integer, primary_key=True)
    )

    op.create_foreign_key(
        'fk_buyers_user',
        'buyers', 'users',
        ['id'], ['id']
    )

    op.add_column('campaign', sa.Column('description', sa.String(255), nullable=False))
    op.add_column('campaign', sa.Column('printer_id', sa.Integer, nullable=False))
    op.add_column('campaign', sa.Column('campaign_picture_url', sa.String(255), nullable=False))
    op.add_column('campaign', sa.Column('pledge_price', sa.DECIMAL, nullable=False))
    op.add_column('campaign', sa.Column('min_pledgers', sa.Integer, nullable=False))
    op.add_column('campaign', sa.Column('max_pledgers', sa.Integer, nullable=True))
    op.add_column('campaign', sa.Column('start_date', sa.DateTime, nullable=False))
    op.add_column('campaign', sa.Column('end_date', sa.DateTime, nullable=False))

    op.create_foreign_key(
        'fk_campaign_printer',
        'campaign', 'printers',
        ['printer_id'], ['id']
    )

    op.create_table(
        'pledges',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('campaign_id', sa.Integer, nullable=False),
        sa.Column('pledge_price', sa.DECIMAL, nullable=False),
        sa.Column('buyer_id', sa.Integer, nullable=False),
        sa.Column('pledge_date', sa.DateTime, nullable=False)
    )

    op.create_foreign_key(
        'fk_pledges_campaign',
        'pledges', 'campaign',
        ['campaign_id'], ['id']
    )

    op.create_foreign_key(
        'fk_pledges_buyer',
        'pledges', 'buyers',
        ['buyer_id'], ['id']
    )

    op.create_table(
        'tech_details',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('campaign_id', sa.Integer, nullable=False),
        sa.Column('material', sa.String(100), nullable=False),
        sa.Column('weight', sa.Integer, nullable=False),
        sa.Column('width', sa.Integer, nullable=False),
        sa.Column('length', sa.Integer, nullable=False),
        sa.Column('depth', sa.Integer, nullable=False)
    )

    op.create_foreign_key(
        'fk_tech_details_campaign',
        'tech_details', 'campaign',
        ['campaign_id'], ['id']
    )

    op.create_table(
        'model_images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('campaign_id', sa.Integer, nullable=False),
        sa.Column('model_picture_url', sa.String(255), nullable=False)
    )

    op.create_foreign_key(
        'fk_model_images_campaign',
        'model_images', 'campaign',
        ['campaign_id'], ['id']
    )


def downgrade():
    op.drop_table('pledges')
    op.drop_table('tech_details')
    op.drop_table('model_images')
    op.drop_table('campaign')
    op.drop_table('printers')
    op.drop_table('buyers')
    op.drop_table('users')
