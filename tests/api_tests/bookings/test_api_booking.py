import pytest

from tests.conftest import get_db_null_pool


@pytest.mark.parametrize(
    'room_id, from_date, to_date, status_code',
    [
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 200),
        (1, "2026-04-15", "2026-04-20", 400),
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
    "room_id, from_date, to_date, booked_rooms", [
        (1, "2026-04-15", "2026-04-20", 1),
        (2, "2026-04-15", "2026-04-20", 2),
        (3, "2026-04-15", "2026-04-20", 3),
    ]
)
async def test_add_booking_get_them(
        room_id,
        from_date,
        to_date,
        booked_rooms,
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
    assert len(result) == booked_rooms