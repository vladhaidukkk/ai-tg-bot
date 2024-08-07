"""Add text ai_type.

Revision ID: 0fc83e0cdbdc
Revises: 3b7cb2841912
Create Date: 2024-08-07 14:47:01.387968+00:00

"""

from typing import Sequence, Union

from alembic import op

revision: str = "0fc83e0cdbdc"
down_revision: Union[str, None] = "3b7cb2841912"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("INSERT INTO ai_types (name) VALUES ('text')")


def downgrade() -> None:
    op.execute("DELETE FROM ai_types WHERE name = 'text'")
