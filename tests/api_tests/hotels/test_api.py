from src.schemas.hotels import HotelOutSchema, HotelSchema


async def test_get_hotels(ac) -> list[HotelOutSchema]:
    response = await ac.get(
        "/hotels/empty_hotels",
        params={
            'from_date': '2026-04-18',
            'to_date': '2026-04-23'
        }
    )
    hotels = response.json()
    for hotel in hotels:
        print(hotel['title'])
    return hotels


async def test_post_hotels(ac) -> HotelOutSchema:
    response = await ac.post(
        "/hotels/",
        json=HotelSchema(
            title='Test Hotel Bishkek',
            location='Testesteron city'
        ).model_dump()
    )
    hotel = response.json()
    print(hotel)
    return hotel