"""Add image ai_models.

Revision ID: bfb6917f1300
Revises: 7390f063c332
Create Date: 2024-08-10 08:59:42.568863+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "bfb6917f1300"
down_revision: Union[str, None] = "7390f063c332"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    type_id = conn.scalar(sa.text("SELECT id FROM ai_types WHERE name = 'image'"))
    # price = image * 1.5
    conn.execute(
        sa.text("""
            INSERT INTO ai_models (name, type_id, price) VALUES
            ('dall-e-2', :type_id, 0.03),
            ('dall-e-3', :type_id, 0.06)
        """),
        {"type_id": type_id},
    )


def downgrade() -> None:
    op.execute("DELETE FROM ai_models WHERE name IN ('dall-e-2', 'dall-e-3')")
