from src.models import RoomsOrm
from src.repositories.base import BaseRepository
from src.models.bookings import BookingsOrm, Status
from src.repositories.mappers.mappers import BookingMapper
from sqlalchemy import select, func
from datetime import date, datetime
from pydantic import BaseModel
from src.schemas.bookings import BookingAddSchema, BookingUpdateRequestSchema, BookingUpdateSchema
from src.exception_handlers.exceptions import NotEmptyRoomsException, ObjectNotFoundException


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

        count = await self.get_booked_count(room_id=data.room_id, from_date=data.from_date, to_date=data.to_date)

        if count >= room.quantity:
            raise NotEmptyRoomsException

        booking = self.model(
            room_id=data.room_id,
            user_id=data.user_id,
            from_date=data.from_date,
            to_date=data.to_date,
            price=room.price * (data.to_date.day - data.from_date.day),
        )
        self.session.add(booking)
        await self.session.flush()
        return booking

    async def edit_booking(self, booking_id: int, user_id: int, data: BookingUpdateRequestSchema):
        room_query = (
            select(RoomsOrm)
            .filter_by(id=data.room_id)
            .with_for_update()
        )
        room_result = await self.session.execute(room_query)
        room = room_result.scalar_one_or_none()
        if not room:
            raise ObjectNotFoundException

        count_booked = await self.get_booked_count(room_id=data.room_id, from_date=data.from_date, to_date=data.to_date)
        if count_booked >= room.quantity:
            raise NotEmptyRoomsException

        _schema_for_update = BookingUpdateSchema(
            price=((data.to_date.day - data.from_date.day) * room.price),
            status=Status.PENDING,
            **data.model_dump()
        )

        return await self.edit(id=booking_id, user_id=user_id, data=_schema_for_update)


    async def get_booked_count(self, room_id: int, from_date: datetime, to_date: datetime):
        result = await self.session.execute(
            select(func.count(BookingsOrm.id))
            .where(
                BookingsOrm.room_id == room_id,
                BookingsOrm.from_date < to_date,
                BookingsOrm.to_date > from_date
            )
        )
        return result.scalar()