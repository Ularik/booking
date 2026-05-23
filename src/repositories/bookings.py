from fastapi import HTTPException
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingMapper
from sqlalchemy import select
from datetime import date
from pydantic import BaseModel
from src.schemas.bookings import BookingAddSchema
from src.repositories.utils import get_free_rooms_ids
from src.exceptions import NotEmptyRoomsException


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingMapper

    async def get_todays_bookings(self) -> list[BaseModel]:
        query = select(self.model).filter(self.model.from_date == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(res) for res in result.scalars()]

    async def add_booking(self, data: BookingAddSchema):
        free_rooms_ids_query = await get_free_rooms_ids(
            from_date=data.from_date,
            to_date=data.to_date,
        )
        result = await self.session.execute(free_rooms_ids_query)
        free_rooms_ids = result.scalars().all()

        if data.room_id not in free_rooms_ids:
            raise NotEmptyRoomsException

        return await super().add_obj(data)
