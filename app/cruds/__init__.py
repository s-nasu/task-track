from typing import Generic, Type, TypeVar
from uuid import UUID

from fastapi import HTTPException, status
from sqlmodel import Session, SQLModel

from models import BaseCreateSchema, BaseUpdateSchema

ModelType = TypeVar("ModelType", bound=SQLModel)

CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseCreateSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseUpdateSchema)


class CRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):

    def __init__(self, model: Type[ModelType], session: Session) -> None:
        self.model = model
        self.session = session

    def create(self, obj_in: CreateSchemaType) -> ModelType:
        object = self.model.model_validate(obj_in)
        self.session.add(object)
        self.session.commit()
        self.session.refresh(object)
        return object

    def get(self, id: UUID) -> ModelType:
        obj = self.session.get(self.model, id)
        if not obj:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Object not found"
            )
        return obj

    def update(self, id: UUID, update_data: UpdateSchemaType) -> ModelType:
        obj = self.get(id)
        model_data = update_data.model_dump(exclude_unset=True)
        for key, value in model_data.items():
            setattr(obj, key, value)
        self.session.add(obj)
        self.session.commit()
        self.session.refresh(obj)
        return obj

    def delete(self, id: UUID) -> ModelType:
        obj = self.get(id)
        self.session.delete(obj)
        self.session.commit()
        return obj
