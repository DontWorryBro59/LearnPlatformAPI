from fastapi import APIRouter, Body, Depends
from myapp.schemas.schemas import SUserSend
from typing import Annotated
users = APIRouter(prefix="/users", tags=["👦users"])

fake_user_db = []

@users.get("/")
async def root() -> dict:
    return {"users": fake_user_db}


@users.post("/add/")
async def add_user(user: Annotated[SUserSend, Body()]) -> dict:
    fake_user_db.append(user)
    message = f"User {user.first_name} {user.last_name} with email {user.email} added"
    return {"message": message}


@users.delete("/del/")
async def delete_user(user: Annotated[SUserSend, Body()]) -> dict:
    fake_user_db.remove(user)
    message = f"User {user.first_name} {user.last_name} with email {user.email} deleted"
    return {"message": message}