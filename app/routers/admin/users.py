from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Field, Session, SQLModel, select

from cruds.user_crud import UserCRUD
from dependencies.database import get_session
from models.todo import Todo, TodoReadSchema, UserReadWithTodosSchema
from models.user import User, UserCreateSchema, UserUpdateSchema


class NotFound(SQLModel):
    detail: str | None = Field(default="ユーザが見つかりません")


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={
        status.HTTP_404_NOT_FOUND: {
            "description": "Not found",
            "model": NotFound,
        },
    },
)


@router.post(
    "",
    response_model=User,
    summary="User作成",
    description="新しいUserを作成する",
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    *,
    user: UserCreateSchema,
    session: Session = Depends(get_session),
):

    user_crud = UserCRUD(session)

    created_user = user_crud.create(user)
    return created_user


@router.get(
    "",
    response_model=List[UserReadWithTodosSchema],
    summary="User一覧取得",
    description="Userの一覧を取得する",
    status_code=status.HTTP_200_OK,
)
async def read_users(
    *,
    session: Session = Depends(get_session),
    offset: int = Query(default=0, description="オフセット", ge=0),
    limit: int = Query(default=100, description="リミット", ge=1, le=100),
):
    query = select(User).offset(offset).limit(limit)
    users = session.exec(query).all()
    return users


@router.get(
    "/{id}",
    response_model=UserReadWithTodosSchema,
    summary="User取得",
    description="指定したIDのUserを取得する",
    status_code=status.HTTP_200_OK,
)
async def read_user(
    *,
    id: UUID,
    session: Session = Depends(get_session),
):

    user_crud = UserCRUD(session)
    return user_crud.get(id)


@router.patch(
    "/{id}",
    summary="User更新",
    description="指定したIDのUserを更新する",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_user(
    *,
    id: UUID,
    user_update: UserUpdateSchema,
    session: Session = Depends(get_session),
):
    user_crud = UserCRUD(session)
    user_crud.update(id, user_update)


@router.delete(
    "/{id}",
    summary="User削除",
    description="指定したIDのUserを削除する",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_user(
    *,
    id: UUID,
    session: Session = Depends(get_session),
):

    user_crud = UserCRUD(session)
    user_crud.delete(id)


@router.get(
    "/{user_id}/todos",
    response_model=List[TodoReadSchema],
    summary="ユーザーの全てのTodoを取得",
    description="指定したユーザーIDに関連する全てのTodoを取得する",
)
async def get_user_todos(
    *,
    user_id: UUID,
    session: Session = Depends(get_session),
):
    todos = session.exec(select(Todo).where(Todo.assignee_id == user_id)).all()
    return todos
