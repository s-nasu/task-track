from enum import Enum
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from dependencies.database import get_session

router = APIRouter(
    prefix="/models",
    tags=["models"],
)


@router.get("/{id}")
async def read_model(id):
    return {"model_id": id}


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


@router.get(
    "/{model_name}",
    summary="Get Model",
    description="Get information about a specific model",
    status_code=status.HTTP_200_OK,
)
async def get_model(model_name: ModelName, session: Session = Depends(get_session)):
    if model_name is ModelName.alexnet:
        return {"model_name": model_name, "message": "Deep Learning FTW!"}
    if model_name.value == "lenet":
        return {"model_name": model_name, "message": "LeCNN all the images"}
    return {"model_name": model_name, "message": "Have some residuals"}
