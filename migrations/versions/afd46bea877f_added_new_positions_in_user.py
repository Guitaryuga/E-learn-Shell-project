"""added new positions in user

Revision ID: afd46bea877f
Revises: 370afb8e6771
Create Date: 2021-01-13 20:00:51.159241

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afd46bea877f'
down_revision = '370afb8e6771'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('fio', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'fio')
    # ### end Alembic commands ###
