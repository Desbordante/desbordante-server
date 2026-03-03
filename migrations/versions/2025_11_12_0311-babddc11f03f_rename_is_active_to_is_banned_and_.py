"""Rename is_active to is_banned and invert values

Revision ID: babddc11f03f
Revises: 453326bf7956
Create Date: 2025-11-12 03:11:01.806687

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "babddc11f03f"
down_revision: Union[str, None] = "453326bf7956"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add new column as nullable first
    op.add_column("users", sa.Column("is_banned", sa.Boolean(), nullable=True))

    # Copy values with inversion: is_banned = NOT is_active
    op.execute("UPDATE users SET is_banned = NOT is_active")

    # Make column not nullable with default value
    op.alter_column("users", "is_banned", nullable=False, server_default=sa.false())

    # Drop old column
    op.drop_column("users", "is_active")


def downgrade() -> None:
    """Downgrade schema."""
    # Add old column as nullable first
    op.add_column("users", sa.Column("is_active", sa.Boolean(), nullable=True))

    # Copy values with inversion: is_active = NOT is_banned
    op.execute("UPDATE users SET is_active = NOT is_banned")

    # Make column not nullable with default value
    op.alter_column("users", "is_active", nullable=False, server_default=sa.true())

    # Drop new column
    op.drop_column("users", "is_banned")
