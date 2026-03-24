from src.services.auth import AuthService


def test_create_access_token():
    data = {"id": 1}
    token = AuthService().create_access_token(data)
    assert token
    assert isinstance(token, str)
