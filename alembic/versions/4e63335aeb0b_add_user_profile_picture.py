"""add user profile picture

Revision ID: 4e63335aeb0b
Revises: c714da18fbbc
Create Date: 2021-08-20 22:55:57.722797

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4e63335aeb0b'
down_revision = 'c714da18fbbc'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('users', sa.Column('profile_picture_url', sa.String(255), nullable=True))


def downgrade():
    op.drop_column('users', 'profile_picture_url')
