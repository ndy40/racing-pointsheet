"""add role to account.Driver entity

Revision ID: cd325168aea2
Revises: 02a1f5fd122b
Create Date: 2025-06-12 21:12:01.002172

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pointsheet

# revision identifiers, used by Alembic.
revision: str = 'cd325168aea2'
down_revision: Union[str, None] = '02a1f5fd122b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('drivers', schema=None) as batch_op:
        batch_op.add_column(sa.Column('role', pointsheet.models.custom_types.UserRoleType, nullable=True))

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('drivers', schema=None) as batch_op:
        batch_op.drop_column('role')

    # ### end Alembic commands ###
