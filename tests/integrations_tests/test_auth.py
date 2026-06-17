from src.services.auth import AuthService


async def test_integration_to_user():
    data = {"id": 1}
    token = await AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)

    payload = await AuthService().encode_token(token)
    assert payload
    assert payload['id'] == data['id']

