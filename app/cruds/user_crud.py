from sqlmodel import Session

from cruds import CRUD
from models.user import User, UserCreateSchema, UserUpdateSchema


class UserCRUD(CRUD[User, UserCreateSchema, UserUpdateSchema]):

    def __init__(self, session: Session):
        super().__init__(User, session=session)
