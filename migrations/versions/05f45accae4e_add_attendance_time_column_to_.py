"""Add attendance_time column to Attendance model

Revision ID: 05f45accae4e
Revises: 88d3a239c042
Create Date: 2024-11-05 23:38:17.276990

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '05f45accae4e'
down_revision = '88d3a239c042'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.add_column(sa.Column('attendance_time', sa.Time(), nullable=False))
        batch_op.alter_column('status',
               existing_type=sa.VARCHAR(length=10),
               type_=sa.String(length=20),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('attendance', schema=None) as batch_op:
        batch_op.alter_column('status',
               existing_type=sa.String(length=20),
               type_=sa.VARCHAR(length=10),
               existing_nullable=False)
        batch_op.drop_column('attendance_time')

    # ### end Alembic commands ###
