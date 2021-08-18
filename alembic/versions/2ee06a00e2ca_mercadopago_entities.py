"""mercadopago entities

Revision ID: 2ee06a00e2ca
Revises: 689c27d921e4
Create Date: 2021-07-15 13:59:56.062032

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ee06a00e2ca'
down_revision = '689c27d921e4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('mp_payment_id', sa.BigInteger, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('amount', sa.DECIMAL, nullable=False),
        sa.Column('type', sa.String(20), nullable=False),
        sa.Column('is_future', sa.Boolean, nullable=False),
    )
    op.create_foreign_key(
        'fk_user_transactions',
        'transactions', 'users',
        ['user_id'], ['id']
    )

    op.add_column('campaign', sa.Column('mp_preference_id', sa.String(255), nullable=True))

    op.add_column('pledges', sa.Column('printer_transaction_id', sa.Integer, nullable=True))
    op.create_foreign_key(
        'fk_printer_pledge_transactions',
        'pledges', 'transactions',
        ['printer_transaction_id'], ['id']
    )

    op.create_table(
        'balance_requests',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', sa.Integer, nullable=False),
        sa.Column('date', sa.DateTime, nullable=False)
    )
    op.create_foreign_key(
        'fk_user_balance_request',
        'balance_requests', 'users',
        ['user_id'], ['id']
    )


def downgrade():
    op.drop_constraint('fk_user_balance_request', 'balance_requests', type_='foreignkey')
    op.drop_table('balance_requests')
    op.drop_constraint('fk_printer_pledge_transactions', 'pledges', type_='foreignkey')
    op.drop_column('pledges', 'printer_transaction_id')
    op.drop_column('campaign', 'mp_preference_id')
    op.drop_constraint('fk_user_transactions', 'transactions', type_='foreignkey')
    op.drop_table('transactions')
