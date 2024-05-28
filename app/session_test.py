from fastapi import Depends
from sqlmodel import Session

import models
from dependencies.database import get_session


def get_db(session: Session = Depends(get_session)):
    session.get(models.todo.Todo, "47833a2a-32ea-4d6d-bed0-09f0aa362e46")
    pass


if __name__ == "__main__":
    print(get_db())
