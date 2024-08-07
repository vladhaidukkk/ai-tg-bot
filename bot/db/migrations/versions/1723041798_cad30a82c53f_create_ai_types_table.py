"""Create ai_types table.

Revision ID: cad30a82c53f
Revises: d5c642daaf2c
Create Date: 2024-08-07 14:43:18.784452+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "cad30a82c53f"
down_revision: Union[str, None] = "d5c642daaf2c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "ai_types",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_ai_types")),
        sa.UniqueConstraint("name", name=op.f("uq_ai_types_name")),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("ai_types")
    # ### end Alembic commands ###