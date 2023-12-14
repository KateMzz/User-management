"""upgraded user with password

Revision ID: a6c960e2bf90
Revises: e550c74872f0
Create Date: 2023-11-27 01:54:10.613481

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a6c960e2bf90"
down_revision: Union[str, None] = "e550c74872f0"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("user", sa.Column("hashed_password", sa.String(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user", "hashed_password")
    # ### end Alembic commands ###
