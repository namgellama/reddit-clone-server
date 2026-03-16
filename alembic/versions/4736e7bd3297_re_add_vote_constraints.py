"""re-add vote constraints

Revision ID: 4736e7bd3297
Revises: 3a829c6ec388
Create Date: 2026-03-16 13:22:13.721925

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "4736e7bd3297"
down_revision: Union[str, Sequence[str], None] = "3a829c6ec388"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_only_one_target",
        "upvotes",
        "(post_id IS NOT NULL AND comment_id IS NULL) OR "
        "(post_id IS NULL AND comment_id IS NOT NULL)",
    )

    op.create_check_constraint(
        "check_only_one_target",
        "downvotes",
        "(post_id IS NOT NULL AND comment_id IS NULL) OR "
        "(post_id IS NULL AND comment_id IS NOT NULL)",
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("check_only_one_target", "upvotes", type_="check")
    op.drop_constraint("check_only_one_target", "downvotes", type_="check")
