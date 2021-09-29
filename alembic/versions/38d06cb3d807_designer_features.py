"""designer features

Revision ID: 38d06cb3d807
Revises: 4e63335aeb0b
Create Date: 2021-08-22 22:07:53.334605

"""
import sqlalchemy as sa
from alembic import op
# revision identifiers, used by Alembic.
from sqlalchemy import func, table, column, Integer, String

revision = '38d06cb3d807'
down_revision = '4e63335aeb0b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'designers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bank_information_id', sa.Integer, nullable=False)
    )

    op.create_foreign_key(
        'fk_designer_user',
        'designers', 'users',
        ['id'], ['id']
    )

    op.create_foreign_key(
        'fk_designer_bank_information',
        'designers', 'bank_information',
        ['bank_information_id'], ['id']
    )

    op.create_table(
        'model_files',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('model_file_url', sa.String(255), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False)
    )

    op.create_table(
        'model_categories',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(255), nullable=False)
    )

    op.create_table(
        'models',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('designer_id', sa.Integer, nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.TEXT, nullable=False),
        sa.Column('model_file_id', sa.Integer, nullable=False),
        sa.Column('model_category_id', sa.Integer, nullable=False),
        sa.Column('likes', sa.Integer, nullable=False),
        sa.Column('width', sa.Integer, nullable=False),
        sa.Column('length', sa.Integer, nullable=False),
        sa.Column('depth', sa.Integer, nullable=False),
        sa.Column('mp_preference_id', sa.String(255), nullable=True),
        sa.Column('allow_purchases', sa.Boolean, nullable=False),
        sa.Column('allow_alliances', sa.Boolean, nullable=False),
        sa.Column('purchase_price', sa.DECIMAL, nullable=True),
        sa.Column('desired_percentage', sa.DECIMAL, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=func.now(), nullable=False),
        sa.Column('deleted_at', sa.DateTime, server_default=func.now(), nullable=True)
    )

    op.create_foreign_key(
        'fk_model_model_categories',
        'models', 'model_categories',
        ['model_category_id'], ['id']
    )

    op.create_foreign_key(
        'fk_model_designer',
        'models', 'designers',
        ['designer_id'], ['id']
    )

    op.create_foreign_key(
        'fk_model_model_files',
        'models', 'model_files',
        ['model_file_id'], ['id']
    )

    op.create_table(
        'model_images',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('model_picture_url', sa.String(255), nullable=False),
        sa.Column('file_name', sa.String(255), nullable=False)
    )

    op.create_foreign_key(
        'fk_model_image_model',
        'model_images', 'models',
        ['model_id'], ['id']
    )

    op.create_table(
        'model_likes',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('user_id', sa.Integer, nullable=False),
    )

    op.create_foreign_key(
        'fk_model_like_model',
        'model_likes', 'models',
        ['model_id'], ['id']
    )

    op.create_foreign_key(
        'fk_model_like_user',
        'model_likes', 'users',
        ['user_id'], ['id']
    )

    op.create_table(
        'model_purchases',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('printer_id', sa.Integer, nullable=False),
        sa.Column('model_id', sa.Integer, nullable=False),
        sa.Column('price', sa.DECIMAL, nullable=False),
        sa.Column('transaction_id', sa.Integer, nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=func.now(), nullable=False),
    )

    op.create_foreign_key(
        'fk_model_purchase_printer',
        'model_purchases', 'printers',
        ['printer_id'], ['id']
    )

    op.create_foreign_key(
        'fk_model_purchase_model',
        'model_purchases', 'models',
        ['model_id'], ['id']
    )

    op.create_foreign_key(
        'fk_model_purchase_transaction',
        'model_purchases', 'transactions',
        ['transaction_id'], ['id']
    )

    model_categories = table('model_categories',
        column('id', Integer),
        column('name', String)
    )

    op.bulk_insert(model_categories, [
        {'id': 1, 'name': 'Videojuegos'},
        {'id': 2, 'name': 'Arquitectura'},
        {'id': 3, 'name': 'Vehículos'},
        {'id': 4, 'name': 'Figuras de acción'},
        {'id': 5, 'name': 'Accesorios'},
        {'id': 6, 'name': 'Hogar'},
        {'id': 7, 'name': 'Electrónica'},
        {'id': 8, 'name': 'Repuestos'},
        {'id': 9, 'name': 'Prótesis'},
        {'id': 10, 'name': 'Plantas'},
        {'id': 11, 'name': 'Deportes'},
        {'id': 12, 'name': 'Otros'}
    ])


def downgrade():
    op.drop_index("fk_model_like_user")
    op.drop_index("fk_model_like_model")
    op.drop_table('model_likes')

    op.drop_index("fk_model_image_model")
    op.drop_table('model_images')

    op.drop_index("fk_model_designer")
    op.drop_table('models')

    op.drop_index("fk_designer_user")
    op.drop_index("fk_designer_bank_information")
    op.drop_table('designers')

    op.drop_index("fk_model_purchase_printer")
    op.drop_index("fk_model_purchase_model")
    op.drop_index("fk_model_purchase_transaction")
    op.drop_table('model_purchases')

    op.drop_table('model_categories')
