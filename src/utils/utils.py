from src.repositories.rooms import RoomsRepository
from src.repositories.hotels import HotelsRepository
from src.repositories.users import UsersRepository
from src.repositories.bookings import BookingsRepository
from src.repositories.facilities import FacilitiesRepository
from src.repositories.facilitiesRooms import RoomsFacilitiesRepository

class DbManager:

    def __init__(self, session_factory):
        self.session_factory = session_factory


    async def __aenter__(self):
        self.session = self.session_factory()
        self.hotelsModel = HotelsRepository(self.session)
        self.roomsModel = RoomsRepository(self.session)
        self.usersModel = UsersRepository(self.session)
        self.bookingsModel = BookingsRepository(self.session)
        self.facilitiesModel = FacilitiesRepository(self.session)
        self.rooms_facilitiesModel = RoomsFacilitiesRepository(self.session)
        return self

    async def __aexit__(self, *args):
        await self.session.rollback()
        await self.session.close()

    async def save(self):
        await self.session.commit()

