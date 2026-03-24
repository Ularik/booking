from src.schemas.hotels import HotelSchema
from src.database import AsyncSession
from src.utils.utils import DbManager


async def test_create_hotel():
    hotel_data = HotelSchema(title="Test Hotel", location="Test country")
    async with DbManager(session_factory=AsyncSession) as db:
        hotel = await db.hotelsModel.add_obj(hotel_data)
        await db.save()
        print(f"New hotel {hotel.title}")