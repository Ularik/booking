from fastapi import APIRouter, Body
from src.schemas.rooms import RoomAddSchema, RoomSchema, RoomEditSchema, RoomAddRequestSchema, RoomEditRequestSchema
from src.schemas.facilities import FacilitiesRoomsAddSchema
from fastapi import Query
from datetime import date
from src.api.dependencies import PaginationDep
from src.api.dependencies import DBDep


router = APIRouter(prefix='/hotels', tags=['Номера'])


@router.get('/{hotel_id}/rooms')
async def get_rooms(
        db: DBDep,
        hotel_id: int,
        paging: PaginationDep,
        from_date: date = Query(date(2026, 3, 16)),
        to_date: date = Query(date(2026, 3, 18))
):
    rooms = await db.roomsModel.get_free_rooms(
        hotel_id=hotel_id,
        from_date=from_date,
        to_date=to_date,
        limit=paging.limit,
        offset=paging.offset
    )
    return rooms


@router.post('/{hotel_id}/rooms', response_model=RoomSchema)
async def add_rooms(
        db: DBDep,
        hotel_id: int,
        data: RoomAddRequestSchema = Body(openapi_examples={
    '1': {
        'summary': "test",
        "description": "test",
        "value": {
            "title": "standard",
            "description": "standard rooms",
            "price": 1500,
            "quantity": 20,
            "facilities": [3, 4]
        }
    }
})):
    _model = RoomAddSchema(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
    room = await db.roomsModel.add_obj(_model)

    room_facilities_data = [FacilitiesRoomsAddSchema(room_id=room.id, facility_id=f) for f in data.facilities]
    await db.rooms_facilitiesModel.add_bulk(room_facilities_data)
    await db.save()
    return room


@router.patch('/{hotel_id}/rooms/{room_id}', response_model=RoomSchema)
async def edit_rooms(
        db: DBDep,
        hotel_id: int,
        room_id: int,
        data: RoomEditRequestSchema = Body(openapi_examples={
    '1': {
        'summary': "test",
        "description": "test",
        "value": {
            "title": "standard",
            "description": "standard rooms",
            "price": 1500,
            "quantity": 20,
            "facilities": [4, 5]
        }
    }
})):
    _data_dict = data.model_dump(exclude_unset=True)
    _model = RoomEditSchema(hotel_id=hotel_id, **_data_dict)
    room = await db.roomsModel.edit(_model, id=room_id, hotel_id=hotel_id)

    if "facilities" in _data_dict:
        await db.rooms_facilitiesModel.set_rooms_facilities(room_id=room_id, facilities=data.facilities)
    await db.save()
    return room


@router.delete('/{hotel_id}/rooms/{room_id}')
async def delete_room(db: DBDep, hotel_id: int, room_id: int):
    await db.roomsModel.delete(id=room_id, hotel_id=hotel_id)
    await db.save()
    return {'delete': 'success'}


