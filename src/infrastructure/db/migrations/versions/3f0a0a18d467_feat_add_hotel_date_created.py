"""feat: add hotel date created

Revision ID: 3f0a0a18d467
Revises: 591d1ac34eae
Create Date: 2025-04-09 00:14:10.523408

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f0a0a18d467"
down_revision: Union[str, None] = "591d1ac34eae"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("hotel", sa.Column("date_created", sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("hotel", "date_created")
    # ### end Alembic commands ###
