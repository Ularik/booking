from src.schemas.rooms import RoomAddRequestSchema


async def test_add_room(ac):
    hotels_response = await ac.get(
        "/hotels/empty_hotels",
        params={
            'from_date': '2026-06-15',
            'to_date': '2026-06-23'
        }
    )
    assert hotels_response.status_code == 200
    hotels = hotels_response.json()

    new_rooms_id = {}
    for hotel in hotels:
        response = await ac.post(
            f'/hotels/{hotel['id']}/rooms',
            json=
            RoomAddRequestSchema(
                title=f'{hotel['id']} {hotel['title']} - Test room',
                description=f"{hotel['id']} {hotel['title']} - Test room",
                price=2100,
                quantity=1
            ).model_dump()
        )

        assert response.status_code == 200
        room = response.json()
        new_rooms_id[hotel['id']] = room['id']

    for hotel_id, room_id in new_rooms_id.items():
        response = await ac.get(
            f'/hotels/{hotel_id}/rooms/{room_id}'
        )
        assert response.status_code == 200


