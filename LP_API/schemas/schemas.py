from re import match
from typing import Annotated

from fastapi import HTTPException, status
from pydantic import BaseModel, EmailStr, Field, AfterValidator

FULL_NAME_PATTERN = '^[A-Za-zА-Яа-я-]+$'


def validate_full_name(value: str) -> str:
    """This function validates first name and last name of the user"""
    if match(FULL_NAME_PATTERN, value):
        return value
    raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Only letters are allowed")


class SUserSend(BaseModel):
    """This is schema for request body"""
    first_name: Annotated[str, AfterValidator(validate_full_name)] = Field(..., max_lenght=150, min_lenght=2,
                                                                           description="Name of the user")
    last_name: Annotated[str, AfterValidator(validate_full_name)] = Field(..., max_lenght=150, min_lenght=2,
                                                                          description="Last name of the user")
    email: EmailStr = Field(..., title="Email of the user", description="Email of the user")
    age: int = Field(..., ge=10, le=120, title="Age of the user", description="Age of the user")


class SUserForORM(SUserSend):
    """This is schema for response from ORM (add ID to parent schema)"""
    id: int = Field(..., title="ID of the user", description="ID of the user")
