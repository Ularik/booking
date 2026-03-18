from watchfiles import awatch

from src.models.rooms import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm
from sqlalchemy import select, func
from src.schemas.hotels import HotelOutSchema
from src.repositories.utils import get_free_rooms_ids


class HotelsRepository(BaseRepository):
    model = HotelsOrm
    schema = HotelOutSchema

    async def get_hotels_with_free_rooms(self, from_date, to_date, title = None, location = None, limit: int = 10, offset: int = 0):
        free_rooms_ids = await get_free_rooms_ids(from_date=from_date, to_date=to_date)

        hotels_ids = (
            select(RoomsOrm.hotel_id)
            .select_from(RoomsOrm)
            .where(RoomsOrm.id.in_(free_rooms_ids))
        )

        filters = []
        if title:
            filters.append(func.lower(HotelsOrm.title).like(f"%{title.lower()}%"))
        if location:
            filters.append(func.lower(HotelsOrm.location).like(f"%{location.lower()}%"))

        return await self.get_filtered_objects(HotelsOrm.id.in_(hotels_ids), *filters, limit=limit, offset=offset)


    async def add_obj(self, data):
        return await super().add_obj(data)
