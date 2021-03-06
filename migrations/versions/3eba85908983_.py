"""empty message

Revision ID: 3eba85908983
Revises: 48508c6d4e99
Create Date: 2020-09-05 18:57:42.338732

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3eba85908983'
down_revision = '48508c6d4e99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currently_reading', sa.Column('date_modified', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currently_reading', 'date_modified')
    # ### end Alembic commands ###
