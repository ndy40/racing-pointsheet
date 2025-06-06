"""add_car_fulltext_search

Revision ID: fdf1a353b4ac
Revises: 75c4f87cbbae
Create Date: 2025-06-06 12:01:39.458563

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fdf1a353b4ac'
down_revision: Union[str, None] = '75c4f87cbbae'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create a virtual FTS5 table for car search
    op.execute("""
        CREATE VIRTUAL TABLE car_fts USING fts5(
            model, 
            year,
            content='cars',
            content_rowid='id'
        )
        """)

    # Populate the FTS table with existing data
    op.execute("""
        INSERT INTO car_fts(car_fts) VALUES('rebuild')
        """)

    # Create triggers to keep the FTS table in sync
    op.execute("""
        CREATE TRIGGER cars_ai AFTER INSERT ON cars
        BEGIN
            INSERT INTO car_fts(car_fts, rowid, model, year)
            VALUES('insert', new.id, new.model, new.year);
        END;
        """)

    op.execute("""
        CREATE TRIGGER cars_ad AFTER DELETE ON cars
        BEGIN
            INSERT INTO car_fts(car_fts, rowid)
            VALUES('delete', old.id);
        END;
        """)

    op.execute("""
        CREATE TRIGGER cars_au AFTER UPDATE ON cars
        BEGIN
            INSERT INTO car_fts(car_fts, rowid)
            VALUES('delete', old.id);
            INSERT INTO car_fts(car_fts, rowid, model, year)
            VALUES('insert', new.id, new.model, new.year);
        END;
        """)



def downgrade() -> None:
    # Drop triggers
    op.execute("DROP TRIGGER IF EXISTS cars_ai")
    op.execute("DROP TRIGGER IF EXISTS cars_ad")
    op.execute("DROP TRIGGER IF EXISTS cars_au")

    # Drop the FTS table
    op.execute("DROP TABLE IF EXISTS car_fts")