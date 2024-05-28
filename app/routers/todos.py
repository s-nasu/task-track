from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query, status
from sqlmodel import Session, select

from cruds.todo_crud import TodoCRUD
from dependencies.database import get_session
from models.todo import Todo, TodoCreateSchema, TodoReadSchema, TodoUpdateSchema

router = APIRouter(
    prefix="/todos",
    tags=["todos"],
)


@router.post(
    "",
    response_model=Todo,
    summary="Todo作成",
    description="新しいTodoを作成する",
    status_code=status.HTTP_201_CREATED,
)
def create_todo(
    *,
    todo: TodoCreateSchema,
    session: Session = Depends(get_session),
):

    todo_crud = TodoCRUD(session)

    created_todo = todo_crud.create(todo)
    return created_todo


@router.get(
    "",
    response_model=List[TodoReadSchema],
    summary="Todo一覧取得",
    description="Todoの一覧を取得する",
    status_code=status.HTTP_200_OK,
)
async def read_todos(
    *,
    session: Session = Depends(get_session),
    offset: int = Query(default=0, description="オフセット", ge=0),
    limit: int = Query(default=100, description="リミット", ge=1, le=100),
    status: Optional[str] = Query(default=None, description="ステータス"),
):
    query = select(Todo).offset(offset).limit(limit)
    if status is not None:
        query = query.where(Todo.status == int(status))
    todos = session.exec(query).all()
    return todos


@router.get(
    "/{id}",
    response_model=TodoReadSchema,
    summary="Todo取得",
    description="指定したIDのTodoを取得する",
    status_code=status.HTTP_200_OK,
)
async def read_todo(
    *,
    id: UUID,
    session: Session = Depends(get_session),
):

    todo_crud = TodoCRUD(session)
    return todo_crud.get(id)


@router.patch(
    "/{id}",
    summary="Todo更新",
    description="指定したIDのTodoを更新する",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def update_todo(
    *,
    id: UUID,
    todo_update: TodoUpdateSchema,
    session: Session = Depends(get_session),
):
    todo_crud = TodoCRUD(session)
    todo_crud.update(id, todo_update)


@router.delete(
    "/{id}",
    summary="Todo削除",
    description="指定したIDのTodoを削除する",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_todo(
    *,
    id: UUID,
    session: Session = Depends(get_session),
):

    todo_crud = TodoCRUD(session)
    todo_crud.delete(id)
