"""signup changes

Revision ID: 689c27d921e4
Revises: d2bb987591c1
Create Date: 2021-07-05 14:47:07.019466

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '689c27d921e4'
down_revision = 'd2bb987591c1'
branch_labels = None
depends_on = None


def upgrade():
    op.create_index(
        index_name='unique_username_idx',
        table_name='users',
        columns=['user_name'],
        unique=True
    )

    op.create_table(
        'bank_information',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('cbu', sa.String(22), nullable=False),
        sa.Column('alias', sa.String(100), nullable=True),
        sa.Column('bank', sa.String(100), nullable=False),
        sa.Column('account_number', sa.String(100), nullable=False),
    )

    op.add_column('printers', sa.Column('bank_information_id', sa.Integer, nullable=False))

    op.create_foreign_key(
        'fk_printers_bank_information',
        'printers', 'bank_information',
        ['bank_information_id'], ['id']
    )


def downgrade():
    op.drop_column('printers', 'bank_information_id')
    op.drop_table('bank_information')
    op.drop_index("unique_username_idx")
