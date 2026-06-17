from src.models import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm
from src.repositories.mappers.mappers import BookingMapper
from sqlalchemy import select, func
from datetime import date
from pydantic import BaseModel
from src.schemas.bookings import BookingAddSchema
from src.exceptions import NotEmptyRoomsException, ObjectNotFoundException


class BookingsRepository(BaseRepository):
    model = BookingsOrm
    mapper = BookingMapper

    async def get_todays_bookings(self) -> list[BaseModel]:
        query = select(self.model).filter(self.model.from_date == date.today())
        result = await self.session.execute(query)
        return [self.mapper.map_to_domain_entity(res) for res in result.scalars()]

    async def add_booking(self, data: BookingAddSchema):

        room_result = await self.session.execute(
            select(RoomsOrm)
            .where(RoomsOrm.id == data.room_id)
            .with_for_update()
        )
        room = room_result.scalar_one_or_none()
        if not room:
            raise ObjectNotFoundException

        count_result = await self.session.execute(
            select(func.count(BookingsOrm.id))
            .where(
                BookingsOrm.room_id == data.room_id,
                BookingsOrm.from_date < data.to_date,
                BookingsOrm.to_date > data.from_date
            )
        )
        count = count_result.scalar()

        if count >= room.quantity:
            raise NotEmptyRoomsException

        booking = self.model(
            room_id=data.room_id,
            user_id=data.user_id,
            from_date=data.from_date,
            to_date=data.to_date,
            price=room.price,
        )
        self.session.add(booking)
        await self.session.flush()  # получаем id без коммита
        return booking