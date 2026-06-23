from src.exception_handlers.exceptions import RoomNotFoundException, NotEmptyRoomsException, ObjectNotFoundException, \
    BookingNotFoundException
from src.schemas.bookings import BookingAddRequestSchema, BookingAddSchema, BookingUpdateRequestSchema, BookingOutSchema
from src.services.base import BaseService
from src.tasks.tasks import check_is_paid

class BookingServices(BaseService):

    async def get_my_bookings(self, user_id: int, limit: int, offset: int) -> list[BookingOutSchema]:

        bookings_list = await self.db.bookingsModel.get_filtered_objects(
            user_id=user_id, limit=limit, offset=offset
        )
        return bookings_list

    async def get_all_bookings(self, limit: int, offset: int):
        bookings_list = await self.db.bookingsModel.get_filtered_objects(
            limit=limit, offset=offset
        )
        return bookings_list

    async def add_booking(self, user_id: int, data: BookingUpdateRequestSchema) -> BookingOutSchema:

        _schema_with_user = BookingAddSchema(user_id=user_id, **data.model_dump())
        try:
            new_booking = await self.db.bookingsModel.add_booking(_schema_with_user)
            await self.db.save()
            check_is_paid.apply_async(
                args=[new_booking.id],
                countdown=15
            )
        except NotEmptyRoomsException:
            raise NotEmptyRoomsException
        except ObjectNotFoundException:
            raise RoomNotFoundException
        return new_booking

    async def delete_booking(self, booking_id: int) -> None:
        try:
            await self.db.bookingsModel.check_exist_delete(id=booking_id)
        except ObjectNotFoundException:
            raise RoomNotFoundException
        await self.db.save()

    async def update_booking(self, user_id: int, booking_id: int, data: BookingUpdateRequestSchema) -> BookingOutSchema:

        try:
            updated_booking = await self.db.bookingsModel.edit_booking(booking_id=booking_id, user_id=user_id, data=data)
            await self.db.save()
            check_is_paid.apply_async(
                args=[updated_booking.id],
                countdown=15
            )
            return updated_booking
        except ObjectNotFoundException as err:
            raise BookingNotFoundException from err
