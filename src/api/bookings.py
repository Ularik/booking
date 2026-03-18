from fastapi.params import Query
from datetime import date
from src.api.dependencies import DBDep, AuthUserDep, PaginationDep
from fastapi import APIRouter, Body
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema


router = APIRouter(prefix="/bookings", tags=["Бронирование"])


@router.get("/me")
async def get_bookings_list(
        user_id: AuthUserDep,
        db: DBDep,
        paging: PaginationDep,
):
    bookings_list = await db.bookingsModel.get_filtered_objects(user_id=user_id,
                                                                limit=paging.limit,
                                                                offset=paging.offset)
    return bookings_list


@router.get("/")
async def get_all_bookings(
        db: DBDep,
        paging: PaginationDep
):
    bookings_list = await db.bookingsModel.get_filtered_objects(limit=paging.limit, offset=paging.offset)
    return bookings_list


@router.post('/')
async def post_bookings(
        user_id: AuthUserDep,
        db: DBDep,
        data: BookingAddRequestSchema = Body(openapi_examples={
    "1": {
        "summary": "",
        "description": "",
        "value": {
            "room_id": 1,
            "from_date": "2026-03-18",
            "to_date": "2026-03-20",
        }
    }
})):
    room = await db.roomsModel.get_one_or_none(id=data.room_id)
    _schema_with_user = BookingAddSchema(user_id=user_id, price=room.price, **data.model_dump())
    new_booking = await db.bookingsModel.add_obj(_schema_with_user)
    await db.save()
    return new_booking


@router.delete('/')
async def delete_bookings(
        user_id: AuthUserDep,
        db: DBDep,
        room_id: int,
        from_date: date = Query(date(2026, 3, 17)),
        to_date: date = Query(date(2026, 3, 23))
):
    await db.bookingsModel.delete(room_id=room_id, from_date=from_date, to_date=to_date)
    await db.save()
    return {'message': "delete success"}