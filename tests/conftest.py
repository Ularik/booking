# ruff: noqa: E402
from typing import AsyncGenerator
from unittest import mock

mock.patch("fastapi_cache.decorator.cache", lambda *args, **kwargs: lambda f: f).start()

from src.main import app
import json
from src.database import Base, engine_null_pool
from src.config import settings
from src.schemas.users import UserOutSchema
from src.models import *  # noqa
import pytest
from httpx import ASGITransport, AsyncClient
from src.schemas.hotels import HotelSchema
from src.schemas.rooms import RoomAddRequestSchema
from src.database import AsyncSessionNullPool
from src.utils.utils import DbManager
from src.api.dependencies import get_db


@pytest.fixture(scope="session", autouse=True)
async def check_mode():
    assert settings.MODE == "TEST"


async def get_db_null_pool() -> AsyncGenerator[DbManager]:
    async with DbManager(session_factory=AsyncSessionNullPool) as db:
        # print("Change DB on DB_NULL_POOL")
        yield db


@pytest.fixture(scope="function")
async def db() -> AsyncGenerator[DbManager]:
    async for db in get_db_null_pool():
        yield db


@pytest.fixture(scope="session", autouse=True)
async def setup_database(check_mode):
    print("-------Fixtures start-----------")
    async with engine_null_pool.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@pytest.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


app.dependency_overrides[get_db] = get_db_null_pool


@pytest.fixture(scope="session", autouse=True)
async def add_user_auth(setup_database, ac) -> UserOutSchema:
    response = await ac.post(
        "/users/",
        json={
            "username": "test_user",
            "nik_name": "test_nikname",
            "password": "admin"
        }
    )
    user = response.json()
    print(response.headers)
    return user


@pytest.fixture(scope="session")
async def authenticate_ac(add_user_auth, ac) -> AsyncGenerator[AsyncClient]:
    await ac.post(
        "/users/login",
        json={
            "username": "test_user",
            "password": "admin"
        }
    )
    assert ac.cookies['access_token']
    yield ac


@pytest.fixture(scope="session", autouse=True)
async def add_hotels(add_user_auth, ac):
    with open('tests/mock_hotel.json', 'r', encoding="utf-8") as f:
        hotels = json.loads(f.read())

        for hotel in hotels:
            _model = HotelSchema(**hotel)
            await ac.post(
                "/hotels/",
                json=_model.model_dump()
            )


@pytest.fixture(scope="session", autouse=True)
async def add_rooms(add_hotels, ac):
    with open('tests/mock_rooms.json', 'r', encoding="utf-8") as f:
        rooms = json.loads(f.read())

        for room in rooms:
            hotel_id = room.pop('hotel_id')
            _model = RoomAddRequestSchema(**room)
            await ac.post(
                f"/hotels/{hotel_id}/rooms",
                json=_model.model_dump()
            )
