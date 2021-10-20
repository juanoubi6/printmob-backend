"""add-percentage-campaign-features

Revision ID: fbfec914e8ff
Revises: 38d06cb3d807
Create Date: 2021-09-13 21:48:52.031020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fbfec914e8ff'
down_revision = '38d06cb3d807'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('pledges', sa.Column('designer_transaction_id', sa.Integer, nullable=True))
    op.create_foreign_key(
        'fk_designer_pledge_transactions',
        'pledges', 'transactions',
        ['designer_transaction_id'], ['id']
    )

    op.add_column('campaign', sa.Column('model_id', sa.Integer, nullable=True))
    op.create_foreign_key(
        'fk_campaign_model',
        'campaign', 'models',
        ['model_id'], ['id']
    )


def downgrade():
    op.drop_index("fk_designer_pledge_transactions")
    op.drop_column('pledges', 'designer_transaction_id')
    op.drop_index("fk_campaign_model")
    op.drop_column('campaign', 'model_id')
