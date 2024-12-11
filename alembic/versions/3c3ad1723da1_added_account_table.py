"""Added account table

Revision ID: 3c3ad1723da1
Revises: 709043220a11
Create Date: 2024-12-09 21:48:41.002076

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "3c3ad1723da1"
down_revision: Union[str, None] = "709043220a11"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Создание таблицы 'histories'
    op.create_table(
        "histories",
        sa.Column(
            "id", sa.Integer(), primary_key=True, autoincrement=True
        ),  # Поле id (auto-increment)
        sa.Column("content_title", sa.String(), nullable=False),  # Поле content_title
        sa.Column("content", sa.String(), nullable=False),  # Поле content
        sa.Column("user_id", sa.Integer(), nullable=False),  # Поле user_id
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),  # Поле created_at
    )


def downgrade():
    # Удаление таблицы 'histories' при откате миграции
    op.drop_table("histories")
