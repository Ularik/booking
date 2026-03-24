from src.services.auth import AuthService


def test_integration_to_user():
    data = {"id": 1}
    token = AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)

    payload = AuthService().encode_token(token)
    print(payload)
    assert payload
    assert payload['id'] == data['id']