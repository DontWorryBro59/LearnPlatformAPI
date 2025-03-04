from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from myapp.database.database_con import get_db
from myapp.database.models import OrmUser
from myapp.schemas.schemas import SUserSend, SUserForORM, SUserForDel

users = APIRouter(prefix="/users", tags=["👦users"])


@users.get("/get/")
async def get_all_users(db: AsyncSession = Depends(get_db)) -> dict:
    query = select(OrmUser)
    result_orm = await db.execute(query)
    result_orm = result_orm.scalars().all()
    result_schema = [SUserForORM.model_validate(item, from_attributes=True) for item in result_orm]
    return {"users": result_schema}


@users.post("/add/")
async def add_user(user: SUserSend, db: AsyncSession = Depends(get_db)) -> dict:
    user_to_add = OrmUser(**user.model_dump())
    db.add(user_to_add)
    await db.commit()
    message = f"Пользователь {user.first_name} {user.second_name} добавлен в базу данных"
    return {"message": message}


@users.delete("/del/")
async def delete_user(user: SUserForDel, db: AsyncSession = Depends(get_db)) -> dict:
    query = select(OrmUser).where(OrmUser.id == user.user_id)
    result_orm = await db.execute(query)
    result_orm = result_orm.scalars().first()
    if not result_orm:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Пользователь с id {user.user_id} не найден")
    print(result_orm.id, result_orm.first_name, result_orm.second_name)
    await db.delete(result_orm)
    await db.commit()
    message = f"Пользователь с id {user.user_id} удален из базы данных"
    return {"message": message}
