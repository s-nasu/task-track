from datetime import datetime
from uuid import UUID, uuid4

import pytz
from sqlmodel import Field, SQLModel


def get_current_time_japan():
    return datetime.now(pytz.timezone("Asia/Tokyo"))


class BaseCreateSchema(SQLModel):
    pass


class BaseUpdateSchema(SQLModel):
    pass


class BaseTable(SQLModel, table=False):
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        index=True,
        nullable=False,
    )
    created_at: datetime | None = Field(
        default=get_current_time_japan(), nullable=False, description="作成日時"
    )
    updated_at: datetime | None = Field(
        default_factory=get_current_time_japan,
        nullable=False,
        description="更新日時",
        sa_column_kwargs={"onupdate": get_current_time_japan},
    )
