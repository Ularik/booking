from src.schemas.hotels import HotelOutSchema


async def test_get_hotels(ac) -> list[HotelOutSchema]:
    response = await ac.get(
        "/hotels/empty_hotels",
        params={
            'from_date': '2026-04-18',
            'to_date': '2026-04-23'
        }
    )
    hotels = response.json()
    print(f"Empty hotels: ")
    for hotel in hotels:
        print(hotel['title'])
    return hotels