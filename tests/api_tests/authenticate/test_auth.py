import pytest
from src.schemas.users import UsersRequestSchema

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

    response = await ac.post(
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
