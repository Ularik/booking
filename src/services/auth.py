from fastapi import HTTPException
from pwdlib import PasswordHash
from datetime import timezone, datetime, timedelta
import jwt
from src.config import settings


class AuthService:
    password_hash = PasswordHash.recommended()

    def create_access_token(self, data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    def hash_pswd(self, password: str) -> str:
        return self.password_hash.hash(password)

    def verify_password(self, plain_password, hashed_password):
        return self.password_hash.verify(plain_password, hashed_password)

    def encode_token(self, token) -> dict:
        try:
            user = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return user
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail="Сессия истекла, войдите снова")
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=401, detail="Некорректный токен доступа")
