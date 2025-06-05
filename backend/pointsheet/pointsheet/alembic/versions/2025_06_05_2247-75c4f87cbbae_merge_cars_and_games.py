"""merge cars and games

Revision ID: 75c4f87cbbae
Revises: 871d28f92662, f2359c0739f8
Create Date: 2025-06-05 22:47:26.424901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '75c4f87cbbae'
down_revision: Union[str, None] = ('871d28f92662', 'f2359c0739f8')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
