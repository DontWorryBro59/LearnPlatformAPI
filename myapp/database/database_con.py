from sqlalchemy.ext.asyncio import create_async_engine

from myapp.database.config_db import Config
from myapp.database.models import Base

config = Config()
# create async engin to connect to database
engine = create_async_engine(url=config.get_db_uri)
test_engine = create_async_engine(url=config.get_test_db_uri, echo=True)


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_all_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
