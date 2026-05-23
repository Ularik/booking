from src.schemas.bookings import BookingAddSchema, BookingUpdateSchema
from datetime import datetime


async def test_bookings(db):
    user = (await db.usersModel.get_objects())[0]
    room = (await db.roomsModel.get_objects())[0]

    _model = BookingAddSchema(
        user_id=user.id,
        room_id=room.id,
        from_date=datetime(year=2026, month=3, day=28),
        to_date=datetime(year=2026, month=3, day=30),
        price=100
    )
    booking = await db.bookingsModel.add_obj(_model)
    await db.save()
    assert booking.id
    print(f"New booking: {booking.id}")

    _updated_data = BookingUpdateSchema(
        user_id=user.id,
        room_id=room.id,
        from_date=datetime(year=2026, month=4, day=8),
        to_date=datetime(year=2026, month=4, day=11),
    )
    await db.bookingsModel.edit(_updated_data, id=booking.id)

    updated_bookings = await db.bookingsModel.get_filtered_objects(id=booking.id)
    assert len(updated_bookings) == 1
    updated_booking = updated_bookings[0]
    assert updated_booking.from_date == _updated_data.from_date
    assert updated_booking.to_date == _updated_data.to_date

    await db.bookingsModel.delete(
        id=updated_booking.id
    )
    await db.save()

    booking = await db.bookingsModel.get_filtered_objects(
        id=updated_booking.id
    )
    assert booking == []
    print("Delete my Booking")