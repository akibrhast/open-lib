"""empty message

Revision ID: 7fd30613f979
Revises: b2a98c8e2fe8
Create Date: 2020-09-05 19:28:16.590705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7fd30613f979'
down_revision = 'b2a98c8e2fe8'
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
