"""create initial applications table

Revision ID: 1bc05e082fc7
Revises: c4d3f78efe46
Create Date: 2026-10-02 17:30:10.973100

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1bc05e082fc7'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("company", sa.String(), nullable=True),
        sa.Column("position", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    op.create_index(
        "ix_applications_id",
        "applications",
        ["id"],
        unique=False,
    )
    op.create_index(
        "ix_applications_company",
        "applications",
        ["company"],
        unique=False,
    )



def downgrade() -> None:
    op.drop_index("ix_applications_company", table_name="applications")
    op.drop_index("ix_applications_id", table_name="applications")
    op.drop_table("applications")