from enum import Enum as PyEnum
from typing import Optional
from uuid import UUID

from sqlmodel import Field, Relationship, SQLModel

from models import BaseCreateSchema, BaseTable, BaseUpdateSchema
from models.extra_types.formatted_datetime import FormattedDatetime
from models.user import UserReadSchema


class TaskStatus(PyEnum):
    TODO = 1
    DOING = 2
    DONE = 3


class TodoBase(SQLModel):
    title: str = Field(index=True, nullable=False, description="タイトル")
    description: Optional[str] = Field(
        default=None, description="説明", max_length=1024
    )
    status: TaskStatus = Field(default=TaskStatus.TODO, description="ステータス")


class Todo(BaseTable, TodoBase, table=True):

    assignee_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id", description="担当者"
    )

    creator_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id", description="作成者"
    )

    updater_id: Optional[UUID] = Field(
        default=None, foreign_key="user.id", description="更新者"
    )
    assignee: Optional["User"] = Relationship(  # noqa: F821
        back_populates="assigned_todos",
        sa_relationship_kwargs={"foreign_keys": "Todo.assignee_id"},
    )

    creator: Optional["User"] = Relationship(  # noqa: F821
        back_populates="created_todos",
        sa_relationship_kwargs={"foreign_keys": "Todo.creator_id"},
    )

    updater: Optional["User"] = Relationship(  # noqa: F821
        back_populates="updated_todos",
        sa_relationship_kwargs={"foreign_keys": "Todo.updater_id"},
    )


class TodoCreateSchema(BaseCreateSchema):
    """
    TodoCreateSchemaクラスは、新しいTodoを作成するためのスキーマです。<br>
    <br>
    Attributes:<br>
        title (str): Todoのタイトル。<br>
        description (Optional[str]): Todoの説明。デフォルトはNoneです。<br>
        status (TaskStatus): Todoのステータス。デフォルトはTaskStatus.TODOです。<br>
        assignee_id (Optional[UUID]): Todoの担当者のID。デフォルトはNoneです。<br>
        creator_id (Optional[UUID]): Todoの作成者のID。デフォルトはNoneです。<br>
        updater_id (Optional[UUID]): Todoの更新者のID。デフォルトはNoneです。<br>
    """

    title: str = Field(index=True, nullable=False, description="タイトル")
    description: Optional[str] = Field(
        default=None, description="説明", max_length=1024
    )
    status: TaskStatus = Field(default=TaskStatus.TODO, description="ステータス")
    assignee_id: Optional[UUID] = Field(default=None, description="担当者")
    creator_id: Optional[UUID] = Field(default=None, description="作成者")
    updater_id: Optional[UUID] = Field(default=None, description="更新者")


class TodoUpdateSchema(BaseUpdateSchema):
    """
    Todoの更新スキーマクラスです。<br>

    Attributes:
        title (Optional[str]): タイトル <br>
        description (Optional[str]): 説明 <br>
        status (TaskStatus): ステータス <br>
        assignee (Optional[str]): 担当者 <br>
        updater (Optional[str]): 更新者 <br>
    """

    title: Optional[str] = Field(default=None, description="タイトル")
    description: Optional[str] = Field(
        default=None, description="説明", max_length=1024
    )
    status: TaskStatus = Field(default=TaskStatus.TODO, description="ステータス")
    assignee_id: Optional[UUID] = Field(default=None, description="担当者")
    updater_id: Optional[UUID] = Field(default=None, description="更新者")


class TodoReadWithTimestampsSchema(TodoBase):
    id: UUID
    created_at: FormattedDatetime = Field(
        description="作成日時 日時の表示形式は%Y-%m-%d %H:%M:%S"
    )
    updated_at: FormattedDatetime = Field(
        description="更新日時 日時の表示形式は%Y-%m-%d %H:%M:%S"
    )


class TodoReadSchema(TodoReadWithTimestampsSchema):
    """
    TodoReadSchemaクラスは、Todoの読み取りスキーマを定義します。<br>
    TodoのAPIの一覧と取得のresponse_modelで使用します。<br>

    <b>属性</b>:<br>
        id (UUID): TodoのID<br>
        assignee (UserReadSchema): 担当者。<br>
        creator (UserReadSchema): 作成者。<br>
        updater (UserReadSchema): 更新者。<br>
        created_at (FormattedDatetime): 作成日時<br>
        updated_at (FormattedDatetime): 更新日時<br>
    <b>TodoBaseから継承した属性</b>:<br>
        title (str): タイトル<br>
        description (str): 説明<br>
        status (TaskStatus): 状態(TODO DOING DONE)<br>
    """

    assignee: UserReadSchema | None = None
    updater: UserReadSchema | None = None
    creator: UserReadSchema | None = None


class UserReadWithTodosSchema(UserReadSchema):
    assigned_todos: list["TodoReadWithTimestampsSchema"] = []  # noqa: F821
