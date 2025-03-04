from typing import Annotated

from fastapi import APIRouter, Body

from myapp.database.database_con import engine
from myapp.database.db_factory import UserRepo
from myapp.schemas.schemas import SUserSend

users = APIRouter(prefix="/users", tags=["👦users"])

fake_user_db = []

db_connection = UserRepo(engine)


@users.get("/get/")
async def get_all_users() -> dict:
    result = await db_connection.get_all_users()
    return {"users": result}


@users.post("/add_user/")
async def add_user(user: Annotated[SUserSend, Body()]) -> dict:
    message = await db_connection.add_user(user)
    return {"message": message}


@users.delete("/del/")
async def delete_user(user_id: Annotated[int, Body()]) -> dict:
    message = await db_connection.delete_user(user_id)
    return {"message": message}
