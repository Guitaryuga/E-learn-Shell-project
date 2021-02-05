"""New columns in Course

Revision ID: 5f02166da3c4
Revises: 
Create Date: 2021-02-01 23:51:17.272699

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5f02166da3c4'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Course', sa.Column('conditions', sa.String(length=64), nullable=True))
    op.add_column('Course', sa.Column('info', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Course', 'info')
    op.drop_column('Course', 'conditions')
    # ### end Alembic commands ###
