from src.schemas.hotels import HotelSchema


async def test_create_hotel(db):
    hotel_data = HotelSchema(title="Test Hotel", location="Test country")
    hotel = await db.hotelsModel.add_obj(hotel_data)
    await db.save()
    print(f"New hotel: {hotel.title}")
