"""empty message

Revision ID: bc77de26374a
Revises: 002f9385d89d
Create Date: 2020-07-10 09:04:00.485938

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc77de26374a'
down_revision = '002f9385d89d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tag',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('lang', sa.Enum('ko', 'en', 'ja', name='tagenum'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tag')
    # ### end Alembic commands ###
