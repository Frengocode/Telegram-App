"""Create user model

Revision ID: fb3408306828
Revises: a9f0053ba78f
Create Date: 2024-11-28 00:57:07.833443

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "fb3408306828"
down_revision: Union[str, None] = "a9f0053ba78f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "messages",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column("message", sa.String(), nullable=False),
        sa.Column("chat_id", sa.Integer(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("is_updated", sa.Boolean(), server_default=sa.text("false")),
    )


def downgrade():
    op.drop_table("messages")
