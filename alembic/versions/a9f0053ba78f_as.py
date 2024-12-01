"""as

Revision ID: a9f0053ba78f
Revises: 
Create Date: 2024-11-28 00:54:29.506830

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a9f0053ba78f"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Create 'users' table with the specified columns
    op.create_table(
        "users",
        sa.Column(
            "id", sa.Integer, primary_key=True
        ),  # Add an 'id' column as the primary key
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("picture_url", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=True),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("age", sa.Integer(), nullable=True),
    )


def downgrade():
    # Drop the 'users' table if rolling back
    op.drop_table("users")
