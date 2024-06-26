"""init create table

Revision ID: 5355a10772ab
Revises:
Create Date: 2024-05-24 01:49:35.310531

"""

from typing import Sequence, Union

import sqlalchemy as sa
import sqlmodel
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "5355a10772ab"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "user",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("name", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("email", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_user_email"), "user", ["email"], unique=True)
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=False)
    op.create_index(op.f("ix_user_name"), "user", ["name"], unique=False)
    op.create_table(
        "todo",
        sa.Column("id", sqlmodel.sql.sqltypes.GUID(), nullable=False),
        sa.Column("title", sqlmodel.sql.sqltypes.AutoString(), nullable=False),
        sa.Column("description", sa.String(1024), nullable=True),
        sa.Column(
            "status",
            sa.Enum("TODO", "DOING", "DONE", name="taskstatus"),
            nullable=False,
        ),
        sa.Column("assignee_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("creator_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("updater_id", sqlmodel.sql.sqltypes.GUID(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(
            ["assignee_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["creator_id"],
            ["user.id"],
        ),
        sa.ForeignKeyConstraint(
            ["updater_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_todo_id"), "todo", ["id"], unique=False)
    op.create_index(op.f("ix_todo_title"), "todo", ["title"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_todo_title"), table_name="todo")
    op.drop_index(op.f("ix_todo_id"), table_name="todo")
    op.drop_table("todo")
    op.drop_index(op.f("ix_user_name"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_index(op.f("ix_user_email"), table_name="user")
    op.drop_table("user")
    # ### end Alembic commands ###
