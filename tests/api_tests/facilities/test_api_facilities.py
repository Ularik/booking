from src.schemas.facilities import FacilitiesSchema


async def add_facilities(ac) -> FacilitiesSchema:
    response = await ac.post(
        '/facilities/',
        json={
            'title': 'PC'
        }
    )
    new_f = response.json()
    assert response.status_code == 200
    print(f"ADD FACILITY: {new_f}")

    return new_f


async def test_get_facilities(ac):
    new_f = await add_facilities(ac)

    response = await ac.get('/facilities/')
    new_f_list = response.json()
    assert new_f_list[0].get('title') == new_f.get('title')
    print(f"GET FACILITY: {new_f}")
