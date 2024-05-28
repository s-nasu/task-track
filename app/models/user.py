from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel

from models import BaseCreateSchema, BaseTable, BaseUpdateSchema
from models.extra_types.formatted_datetime import FormattedDatetime


class UserBase(SQLModel):
    name: str = Field(
        max_length=50, index=True, nullable=False, description="ユーザー名"
    )
    email: str = Field(unique=True, index=True, description="メールアドレス")


class User(BaseTable, UserBase, table=True):
    assigned_todos: List["Todo"] = Relationship(  # noqa: F821
        back_populates="assignee",
        sa_relationship_kwargs={
            "foreign_keys": "Todo.assignee_id",
            "lazy": "selectin",
        },
    )
    created_todos: List["Todo"] = Relationship(  # noqa: F821
        back_populates="creator",
        sa_relationship_kwargs={
            "foreign_keys": "Todo.creator_id",
            "lazy": "selectin",
        },
    )
    updated_todos: List["Todo"] = Relationship(  # noqa: F821
        back_populates="updater",
        sa_relationship_kwargs={
            "foreign_keys": "Todo.updater_id",
            "lazy": "selectin",
        },
    )


class UserCreateSchema(BaseCreateSchema, UserBase):
    email: EmailStr


class UserUpdateSchema(BaseUpdateSchema, SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class UserReadSchema(UserBase):
    id: UUID
    created_at: FormattedDatetime = Field(
        description="作成日時 日時の表示形式は%Y-%m-%d %H:%M:%S"
    )
    updated_at: FormattedDatetime = Field(
        description="更新日時 日時の表示形式は%Y-%m-%d %H:%M:%S"
    )
