import time

import pytest
import asyncio


async def quick_ticker():
    for i in range(5):
        print(f"⏰ [Таймер] Я работаю свободно, тик {i}")
        await asyncio.sleep(0.5)


@pytest.mark.asyncio
async def test_auth_event_loop(ac):
    users = [
        ('user1', 'user1'),
        ('user2', 'user2'),
        ('user3', 'user3'),
        ('user4', 'user4'),
        ('user5', 'user5'),
        ('user6', 'user6'),
        ('user7', 'user7'),
        ('user8', 'user8'),

    ]
    start_time = time.time()

    results = await asyncio.gather(
        *[ac.post(
        "/users/",
            json={
                'username': username,
                'password': password
        }) for username, password in users]
    )
    statuses = [r.status_code for r in results if not isinstance(r, Exception)]

    successful = statuses.count(200)
    assert successful == 8

    end_time = time.time()
    print(f"Авторизация трёх польщователей закончилась за {end_time - start_time} - сек")


@pytest.mark.parametrize(
    "username, password", [
        ('admin', 'admin'),
        ('user', 'user')
    ]
)
async def test_auth_end_to_end(
        username,
        password,
        ac
):
    response = await ac.post(
        "/users/",
        json={
            'username': username,
            'password': password
        }
    )

    assert response.status_code == 200

    await ac.post(
        '/users/login',
        json={
            'username': username,
            'password': password
        }
    )
    assert 'access_token' in ac.cookies

    response = await ac.get(
        '/users/me'
    )

    assert isinstance(response.json(), int)

    await ac.post(
        '/users/logout'
    )

    assert 'access_token' not in ac.cookies
