from re import match
from typing import Annotated

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, AfterValidator

FULL_NAME_PATTERN = '^[A-Za-zА-Яа-я-]+$'


def validate_full_name(value: str) -> str:
    """This function validates name and last name of the user"""
    if match(FULL_NAME_PATTERN, value):
        return value
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only letters are allowed")


class SUserSend(BaseModel):
    """This is schema for request body"""
    first_name: Annotated[str, AfterValidator(validate_full_name)] = Field(...,  min_length=2, max_length=150)
    second_name: Annotated[str, AfterValidator(validate_full_name)] = Field(...,  min_length=2, max_length=150)
    email: EmailStr = Field(..., title="Email of the user", description="Email of the user")
    age: int = Field(..., ge=10, le=120, title="Age of the user", description="Age of the user")


class SUserForORM(SUserSend):
    """This is schema for response from ORM (add ID to parent schema)"""
    id: int = Field(..., title="ID of the user", description="ID of the user")


class SUserForDel(BaseModel):
    user_id: int = Field(..., gt=0)