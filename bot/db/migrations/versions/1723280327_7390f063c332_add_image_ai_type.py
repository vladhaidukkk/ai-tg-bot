"""Add image ai_type.

Revision ID: 7390f063c332
Revises: 58ccaf27d502
Create Date: 2024-08-10 08:58:47.471771+00:00

"""

from typing import Sequence, Union

from alembic import op

revision: str = "7390f063c332"
down_revision: Union[str, None] = "58ccaf27d502"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO ai_types (name) VALUES ('image')")


def downgrade() -> None:
    op.execute("DELETE FROM ai_types WHERE name = 'text'")
