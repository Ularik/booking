import pytest
from src.main import app
from httpx import ASGITransport, AsyncClient
from tests.conftest import get_db_null_pool
import asyncio


@pytest.mark.asyncio
async def test_booking_race_condition():
    """
    Ситуация когда N пользователей одновременно бронируют
    комнату с quantity=5 — только 5 броней должны пройти
    """
    room_id = 1  # комната с quantity=5

    booking_data = {
        "room_id": room_id,
        "from_date": "2025-06-16",
        "to_date": "2025-06-20",
    }

    async def create_book(i):
        async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
            await ac.post(
                '/users/login',
                json={
                    'username': f'user{i}',
                    'password': f'user{i}'
                }
            )
            response = await ac.post(
                '/bookings/',
                json=booking_data
            )
        return response

    responses = await asyncio.gather(
        *[create_book(i) for i in range(1, 9)],
        return_exceptions=True
    )

    statuses = [r.status_code for r in responses if not isinstance(r, Exception)]
    successful = statuses.count(200)
    failed = statuses.count(409)

    print(f"Успешных броней: {successful}, отказов: {failed}")

    assert successful == 5, f"Ожидали 5 успешных бронь, получили {successful}"
    assert failed == 3


@pytest.mark.parametrize(
    'room_id, from_date, to_date, status_code',
    [
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 409),
    ]
)
async def test_create_booking(
        room_id,
        from_date,
        to_date,
        status_code,
        authenticate_ac,
        db
):
    response = await authenticate_ac.post(
        '/bookings/',
        json={
            'room_id': room_id,
            'from_date': from_date,
            'to_date': to_date
        }
    )
    assert response.status_code == status_code


@pytest.fixture(scope="module", autouse=False)
async def delete_bookings():
    async for _db in get_db_null_pool():
        await _db.bookingsModel.delete()
        await _db.save()


@pytest.mark.parametrize(
    "room_id, from_date, to_date, booked_rooms_id", [
        (1, "2026-06-15", "2026-06-20", 1),
        (2, "2026-06-15", "2026-06-20", 2),
        (3, "2026-06-15", "2026-06-20", 3),
    ]
)
async def test_add_booking_get_them(
        room_id,
        from_date,
        to_date,
        booked_rooms_id,
        delete_bookings,
        authenticate_ac
):
    response = await authenticate_ac.post(
        '/bookings/',
        json={
            'room_id': room_id,
            'from_date': from_date,
            'to_date': to_date
        }
    )
    assert response.status_code == 200

    result = await authenticate_ac.get(
        '/bookings/me',
    )
    assert result.status_code == 200
    result = result.json()
    assert len(result) == booked_rooms_id