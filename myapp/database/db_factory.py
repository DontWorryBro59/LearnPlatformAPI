from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy import select
from myapp.database.models import OrmUser
from myapp.schemas.schemas import SUserForORM, SUserSend



class UserRepo:
    def __init__(self, engine):
        self._engine = engine
        self._async_session = async_sessionmaker(engine)

    async def get_all_users(self) -> list[SUserForORM]:
        async with self._async_session() as session:
            query = select(OrmUser)
            result_orm = await session.execute(query)
            result_orm = result_orm.scalars().all()
            result_schema = [SUserForORM.model_validate(item, from_attributes=True) for item in result_orm]
            return result_schema

    async def add_user(self, user: SUserSend) -> str:
        async with self._async_session() as session:
            user_to_add = OrmUser(**user.model_dump())
            session.add(user_to_add)
            await session.commit()
            return f"Пользователь {user.first_name} {user.second_name} добавлен в базу данных"

    async def delete_user(self, user_id: int) -> str:
        async with self._async_session() as session:
            query = select(OrmUser).where(OrmUser.id == user_id)
            result_orm = await session.execute(query)
            result_orm = result_orm.scalars().first()
            if result_orm is None:
                return f"Пользователь с id {user_id} не найден"
            await session.delete(result_orm)
            await session.commit()
            return f"Пользователь с id {user_id} удален из базы данных"