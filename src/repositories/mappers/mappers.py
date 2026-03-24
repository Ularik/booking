from src.repositories.mappers.base import DataMapper
from src.models.hotels import HotelsOrm
from src.models.rooms import RoomsOrm
from src.models.bookings import BookingsOrm
from src.models.users import UserOrm
from src.models.facilities import FacilitiesOrm, RoomsFacilitiesOrm
from src.schemas.hotels import HotelOutSchema
from src.schemas.rooms import RoomSchema, RoomRelSchema
from src.schemas.bookings import BookingOutSchema
from src.schemas.users import UserOutSchema
from src.schemas.facilities import FacilitiesSchema, FacilitiesRoomsSchema


class HotelMapper(DataMapper):
    model = HotelsOrm
    schema = HotelOutSchema


class RoomMapper(DataMapper):
    model = RoomsOrm
    schema = RoomSchema


class RoomRelMapper(DataMapper):
    model = RoomsOrm
    schema = RoomRelSchema


class BookingMapper(DataMapper):
    model = BookingsOrm
    schema = BookingOutSchema


class UserMapper(DataMapper):
    model = UserOrm
    schema = UserOutSchema


class FacilityMapper(DataMapper):
    model = FacilitiesOrm
    schema = FacilitiesSchema


class FacilityRoomMapper(DataMapper):
    model = RoomsFacilitiesOrm
    schema = FacilitiesRoomsSchema