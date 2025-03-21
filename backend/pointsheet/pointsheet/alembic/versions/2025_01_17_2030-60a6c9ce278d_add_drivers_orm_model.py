"""add_drivers_orm_model

Revision ID: 60a6c9ce278d
Revises: 2311a1a16f7e
Create Date: 2025-01-17 20:30:39.469000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pointsheet

# revision identifiers, used by Alembic.
revision: str = "60a6c9ce278d"
down_revision: Union[str, None] = "2311a1a16f7e"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "drivers",
        sa.Column("id", pointsheet.models.custom_types.EntityIdType, nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column(
            "event_id", pointsheet.models.custom_types.EntityIdType, nullable=False
        ),
        sa.ForeignKeyConstraint(
            ["event_id"], ["events.id"], name="drivers_event", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("drivers")
    # ### end Alembic commands ###
