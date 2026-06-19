from src.exceptions import ObjectNotFoundException, NotEmptyRoomsException
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema
from src.services.base import BaseService
from datetime import date
from src.tasks.tasks import check_is_paid

class BookingServices(BaseService):

    async def get_my_bookings(self, user_id: int, limit: int, offset: int):

        bookings_list = await self.db.bookingsModel.get_filtered_objects(
            user_id=user_id, limit=limit, offset=offset
        )
        return bookings_list

    async def get_all_bookings(self, limit: int, offset: int):
        bookings_list = await self.db.bookingsModel.get_filtered_objects(
            limit=limit, offset=offset
        )
        return bookings_list

    async def add_booking(self, user_id: int, data: BookingAddRequestSchema):

        _schema_with_user = BookingAddSchema(user_id=user_id, **data.model_dump())
        try:
            new_booking = await self.db.bookingsModel.add_booking(_schema_with_user)
            await self.db.save()
            result = check_is_paid.apply_async(
                args=[new_booking.id],
                countdown=15
            )
        except NotEmptyRoomsException as ex:
            raise NotEmptyRoomsException
        except ObjectNotFoundException:
            raise ObjectNotFoundException
        return new_booking

    async def delete_booking(self, room_id: int, from_date: date, to_date: date):
        await self.db.bookingsModel.delete(room_id=room_id, from_date=from_date, to_date=to_date)
        await self.db.save()
