from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from myapp.database.config_db import Config
from myapp.database.models import Base

config = Config()
# create async engin to connect to database
engine = create_async_engine(url=config.get_db_uri)
test_engine = create_async_engine(url=config.get_test_db_uri)


local_session = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def _drop_all_table():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db():
    database = local_session()
    try:
        yield database
    finally:
        await database.close()
