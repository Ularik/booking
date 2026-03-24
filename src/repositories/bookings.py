from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingMapper
from sqlalchemy import select
from datetime import date
from pydantic import BaseModel


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingMapper

    async def get_todays_bookings(self) -> list[BaseModel]:
        query = (
            select(self.model)
            .filter(self.model.from_date == date.today())
        )
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(res) for res in result.scalars()]