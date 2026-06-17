from src.services.base import BaseService
from src.schemas.hotels import HotelSchema, HotelsEditSchema
from datetime import date

class HotelsServices(BaseService):

    async def add_hotel(self, data: HotelSchema):
        return await self.db.hotelsModel.add_obj(data)

    async def get_empty_hotels(self,
                               from_date: date,
                               to_date: date,
                               title: str | None = None,
                               location: str | None = None,
                               limit: int = 10,
                               offset: int = 0):
        return await self.db.hotelsModel.get_hotels_with_free_rooms(from_date, to_date, title, location, limit, offset)

    async def get_one_hotel(self, hotel_id: int):
        return await self.db.hotelsModel.get_one(id=hotel_id)

    async def path_hotel(self, data: HotelsEditSchema, hotel_id):
        return await self.db.hotelsModel.edit(data=data, id=hotel_id, exclude_unset=True)

    async def delete_hotel(self, hotel_id):
        await self.db.hotelsModel.check_exist_delete(id=hotel_id)