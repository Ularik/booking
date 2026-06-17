from fastapi import APIRouter, Body, HTTPException
from fastapi_cache.decorator import cache
from fastapi import Query
from datetime import date
from src.services.rooms import RoomsService
from src.schemas.rooms import (
    RoomAddSchema,
    RoomSchema,
    RoomEditSchema,
    RoomAddRequestSchema,
    RoomEditRequestSchema,
)
from src.schemas.facilities import FacilitiesRoomsAddSchema
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep
from src.exceptions import NotValidTimedeltaException, ObjectNotFoundException, UniqueObjIsExistException, \
    RoomAlreadyExistException, HotelNotFoundException

router = APIRouter(prefix="/hotels", tags=["Номера"])


@router.get("/{hotel_id}/rooms")
@cache(expire=15)
async def get_rooms(
    db: DBDep,
    hotel_id: int,
    paging: PaginationDep,
    from_date: date = Query(date(2026, 3, 16)),
    to_date: date = Query(date(2026, 3, 18)),
):
    try:
        rooms = await RoomsService(db).get_rooms(
            hotel_id=hotel_id,
            from_date=from_date,
            to_date=to_date,
            limit=paging.limit,
            offset=paging.offset,
        )
        return rooms
    except NotValidTimedeltaException as err:
        raise HTTPException(400, detail=err.detail)


@router.get("/{hotel_id}/rooms/{room_id}")
@cache(expire=15)
async def get_one_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        rooms = await RoomsService(db).get_one_room(hotel_id=hotel_id, room_id=room_id)
    except ObjectNotFoundException as err:
        raise HTTPException(400, detail=err.detail)
    return rooms


@router.post("/{hotel_id}/rooms", response_model=RoomSchema)
async def add_rooms(
    db: DBDep,
    hotel_id: int,
    data: RoomAddRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "test",
                "description": "test",
                "value": {
                    "title": "standard",
                    "description": "standard rooms",
                    "price": 1500,
                    "quantity": 20,
                    "facilities": [3, 4],
                },
            }
        }
    ),
):
    try:
        room = await RoomsService(db).add_room(hotel_id=hotel_id, data=data)
    except (RoomAlreadyExistException, HotelNotFoundException) as err:
        raise HTTPException(404, detail=err.detail)
    return room


@router.patch("/{hotel_id}/rooms/{room_id}", response_model=RoomSchema)
async def edit_rooms(
    db: DBDep,
    hotel_id: int,
    room_id: int,
    data: RoomEditRequestSchema = Body(
        openapi_examples={
            "1": {
                "summary": "test",
                "description": "test",
                "value": {
                    "title": "standard",
                    "description": "standard rooms",
                    "price": 1500,
                    "quantity": 20,
                    "facilities": [4, 5],
                },
            }
        }
    ),
):
    try:
        room = await RoomsService(db).edit_room(data=data, hotel_id=hotel_id, room_id=room_id)
    except ObjectNotFoundException as err:
        raise HTTPException(status_code=404, detail=err.detail)
    return room


@router.delete("/{hotel_id}/rooms/{room_id}")
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    try:
        await RoomsService(db).delete_room(room_id=room_id, hotel_id=hotel_id)
    except ObjectNotFoundException as err:
        raise HTTPException(404, detail=err.detail)
    await db.save()
    return {"delete": "Удалили номер"}
