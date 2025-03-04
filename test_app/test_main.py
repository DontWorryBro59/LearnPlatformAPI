import asyncio

import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import async_sessionmaker

from myapp.database.database_con import test_engine, get_db
from myapp.main import app

_test_async_session = async_sessionmaker(test_engine)


# Подключение для тестовой базы данных
async def override_get_db():
    db = _test_async_session()
    try:
        yield db
    finally:
        await db.close()


app.dependency_overrides[get_db] = override_get_db



@pytest.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.mark.asyncio
async def test_read_root():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {'message': 'Server is running'}


@pytest.mark.asyncio
async def test_read_user():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get("/users/get/")
    assert response.status_code == 200
    assert response.json() == {'users': []}


@pytest.mark.asyncio
async def test_create_user():
    user = {
        'first_name': 'John',
        'second_name': 'Doe',
        'email': 'john@example.com',
        'age': 30
    }
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.post('/users/add/', json=user)
    assert response.status_code == 200
    assert response.json() == {'message': 'Пользователь John Doe добавлен в базу данных'}


@pytest.mark.asyncio
async def test_del_user():
    async with AsyncClient(transport=ASGITransport(app=app),
                           base_url="http://test") as ac:
        response = await ac.get('/users/get/')
        get_user_id = response.json()['users'][0]['id']
        response = await ac.request("DELETE", "/users/del/", json={'user_id': get_user_id})
    assert response.status_code == 200
    assert response.json() == {'message': f'Пользователь с id {get_user_id} удален из базы данных'}
