"""add_buyer_address

Revision ID: 4214f8990ffc
Revises: bb2106410b34
Create Date: 2021-06-27 18:08:36.314306

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4214f8990ffc'
down_revision = 'bb2106410b34'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('address', sa.String(255), nullable=False),
        sa.Column('floor', sa.String(10), nullable=True),
        sa.Column('apartment', sa.String(10), nullable=True),
        sa.Column('zip_code', sa.String(10), nullable=False),
        sa.Column('province', sa.String(255), nullable=False),
        sa.Column('city', sa.String(255), nullable=False)
    )

    op.add_column('buyers', sa.Column('address_id', sa.Integer, nullable=False))

    op.create_foreign_key(
        'fk_buyer_address',
        'buyers', 'addresses',
        ['address_id'], ['id']
    )

    op.create_table(
        'orders',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('campaign_id', sa.Integer, nullable=False),
        sa.Column('pledge_id', sa.Integer, nullable=False),
        sa.Column('buyer_id', sa.Integer, nullable=False),
        sa.Column('status', sa.String(100), nullable=False),
        sa.Column('mail_company', sa.String(100), nullable=True),
        sa.Column('tracking_code', sa.String(255), nullable=True),
        sa.Column('comments', sa.String(255), nullable=True)
    )

    op.create_foreign_key(
        'fk_orders_campaign',
        'orders', 'campaign',
        ['campaign_id'], ['id']
    )

    op.create_foreign_key(
        'fk_orders_pledge',
        'orders', 'pledges',
        ['pledge_id'], ['id']
    )

    op.create_foreign_key(
        'fk_orders_buyers',
        'orders', 'buyers',
        ['buyer_id'], ['id']
    )


def downgrade():
    op.drop_column('buyers', 'address_id')
    op.drop_table('addresses')
    op.drop_table('orders')
