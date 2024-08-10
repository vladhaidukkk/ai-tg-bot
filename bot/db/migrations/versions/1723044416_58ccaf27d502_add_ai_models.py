"""Add ai_models.

Revision ID: 58ccaf27d502
Revises: 0fc83e0cdbdc
Create Date: 2024-08-07 15:26:56.040117+00:00

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "58ccaf27d502"
down_revision: Union[str, None] = "0fc83e0cdbdc"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    type_id = conn.scalar(sa.text("SELECT id FROM ai_types WHERE name = 'text'"))
    # price = (input_token + output_token) * 1.5
    conn.execute(
        sa.text("""
            INSERT INTO ai_models (name, type_id, price) VALUES
            ('gpt-3.5-turbo', :type_id, 0.0000135),
            ('gpt-4', :type_id, 0.000135),
            ('gpt-4-turbo', :type_id, 0.00006),
            ('gpt-4o', :type_id, 0.00003),
            ('gpt-4o-mini', :type_id, 0.000001125)
        """),
        {"type_id": type_id},
    )


def downgrade() -> None:
    op.execute("""
        DELETE FROM ai_models 
        WHERE name IN (
            'gpt-3.5-turbo', 
            'gpt-4', 
            'gpt-4-turbo', 
            'gpt-4o', 
            'gpt-4o-mini'
        )
    """)
