"""empty message

Revision ID: 97d0e808d55f
Revises: 3eba85908983
Create Date: 2020-09-05 19:16:09.320286

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '97d0e808d55f'
down_revision = '3eba85908983'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('currently_reading', 'date_modified')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('currently_reading', sa.Column('date_modified', postgresql.TIMESTAMP(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
