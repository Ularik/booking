from src.exception_handlers.exceptions import UniqueObjIsExistException, ObjectNotFoundException, HotelNotFoundException, \
    RoomAlreadyExistException
from src.schemas.facilities import FacilitiesRoomsAddSchema
from src.schemas.rooms import RoomAddRequestSchema, RoomAddSchema, RoomEditSchema, RoomEditRequestSchema
from src.services.base import BaseService
from datetime import date

class RoomsService(BaseService):

    async def get_rooms(self,
                        hotel_id: int,
                        from_date: date,
                        to_date: date,
                        limit: int,
                        offset: int):
        return await self.db.roomsModel.get_free_rooms(
            hotel_id=hotel_id,
            from_date=from_date,
            to_date=to_date,
            limit=limit,
            offset=offset,
        )

    async def get_one_room(self, room_id: int, hotel_id: int):
        return await self.db.roomsModel.get_one(hotel_id=hotel_id, room_id=room_id)

    async def add_room(self, hotel_id: int, data: RoomAddRequestSchema):
        _model = RoomAddSchema(hotel_id=hotel_id, **data.model_dump(exclude_unset=True))
        try:
            room = await self.db.roomsModel.add_obj(_model)
        except UniqueObjIsExistException:
            raise RoomAlreadyExistException
        except ObjectNotFoundException:
            raise HotelNotFoundException

        if data.facilities:
            room_facilities_data = [
                FacilitiesRoomsAddSchema(room_id=room.id, facility_id=f) for f in data.facilities
            ]
            await self.db.rooms_facilitiesModel.add_bulk(room_facilities_data)

        await self.db.save()
        return room

    async def edit_room(self, data: RoomEditRequestSchema, hotel_id: int, room_id: int):
        _data_dict = data.model_dump(exclude_unset=True)
        _model = RoomEditSchema(hotel_id=hotel_id, **_data_dict)
        room = await self.db.roomsModel.edit(_model, id=room_id, hotel_id=hotel_id)

        if "facilities" in _data_dict:
            await self.db.rooms_facilitiesModel.set_rooms_facilities(
                room_id=room_id, facilities=data.facilities
            )
        await self.db.save()
        return room

    async def delete_room(self, room_id: int, hotel_id: int):
        self.db.roomsModel.check_exist_delete(id=room_id, hotel_id=hotel_id)