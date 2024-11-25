"""Create tables

Revision ID: 391146e0ffcd
Revises:
Create Date: 2024-11-23 19:32:54.879035

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "391146e0ffcd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

_ = sa


def upgrade() -> None:
    op.execute("""
    CREATE TABLE items (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        blob JSON,
        PRIMARY KEY (id)
    )""")
    op.execute("""
    CREATE TABLE sets (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        PRIMARY KEY (id)
    )""")
    op.execute("""
    CREATE TABLE set_items (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        base_item_id INTEGER,
        set_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(base_item_id) REFERENCES items (id),
        FOREIGN KEY(set_id) REFERENCES sets (id)
    )""")
    op.execute("""
    CREATE TABLE unique_items (
        id INTEGER NOT NULL,
        name VARCHAR NOT NULL,
        base_item_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(base_item_id) REFERENCES items (id)
    )
    """)


def downgrade() -> None:
    op.drop_table("unique_items")
    op.drop_table("set_items")
    op.drop_table("sets")
    op.drop_table("items")
