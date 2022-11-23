from datetime import datetime
from typing import Optional

from fastapi_users import schemas
from pydantic import BaseModel, PositiveFloat


class Operation(BaseModel):
    amount: PositiveFloat
    name: str
    surname: str
    patronymic: str


class OperationDB(Operation):
    id: int
    create_date: datetime
    user_from: int
    commit: bool
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class OperationCreate(Operation):
    pass


class UserRead(schemas.BaseUser[int]):
    name: str
    surname: str
    patronymic: str
    balance: PositiveFloat


class UserCreate(schemas.BaseUserCreate):
    name: str
    surname: str
    patronymic: str
    balance: PositiveFloat


class UserUpdate(schemas.BaseUserUpdate):
    pass
