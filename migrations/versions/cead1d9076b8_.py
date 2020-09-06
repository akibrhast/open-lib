"""empty message

Revision ID: cead1d9076b8
Revises: 97d0e808d55f
Create Date: 2020-09-05 19:16:45.028706

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cead1d9076b8'
down_revision = '97d0e808d55f'
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
