from sqlmodel import Session

from cruds import CRUD
from models.todo import Todo, TodoCreateSchema, TodoUpdateSchema


class TodoCRUD(CRUD[Todo, TodoCreateSchema, TodoUpdateSchema]):

    def __init__(self, session: Session):
        super().__init__(Todo, session=session)
