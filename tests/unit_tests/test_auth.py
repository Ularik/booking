from src.services.auth import AuthService


async def test_create_access_token():
    data = {"id": 1}
    token = await AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)
