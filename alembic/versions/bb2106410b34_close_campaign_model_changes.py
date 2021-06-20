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

    op.create_table(
        'failed_to_refund_pledges',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('pledge_id', sa.Integer, nullable=False),
        sa.Column('fail_date', sa.DateTime, nullable=False),
        sa.Column('error', sa.String(1000), nullable=False),
    )

    op.create_foreign_key(
        'fk_failed_to_refund_pledges_pledge',
        'failed_to_refund_pledges', 'pledges',
        ['pledge_id'], ['id']
    )


def downgrade():
    op.drop_column('campaign', 'status')
    op.drop_table('failed_to_refund_pledges')

