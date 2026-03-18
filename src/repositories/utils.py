from datetime import date
from sqlalchemy import select, func
from src.models.bookings import BookingsOrm
from src.models.rooms import RoomsOrm


async def get_free_rooms_ids(
        from_date: date,
        to_date: date,
        hotel_id: int = None):

    booked_rooms_count = (
        select(
            BookingsOrm.room_id.label("booked_rooms_id"),
            func.count("*").label("booked_count")
        )
        .select_from(BookingsOrm)
        .where(
            BookingsOrm.from_date <= to_date,
               BookingsOrm.to_date >= from_date)
        .group_by(BookingsOrm.room_id)
        .cte(name="booked_rooms")
    )

    rooms_and_quantity = (
        select(
            RoomsOrm.id.label("rooms_id"),
            (RoomsOrm.quantity - func.coalesce(booked_rooms_count.c.booked_count, 0)).label("free_rooms_count")
        )
        .select_from(RoomsOrm)
        .outerjoin(booked_rooms_count, booked_rooms_count.c.booked_rooms_id == RoomsOrm.id)
    )

    if hotel_id:
        rooms_and_quantity = rooms_and_quantity.filter(RoomsOrm.hotel_id == hotel_id)

    free_rooms_ids = (
        select(rooms_and_quantity.c.rooms_id)
        .select_from(rooms_and_quantity)
        .where(rooms_and_quantity.c.free_rooms_count > 0)
    )

    return free_rooms_ids