from fastapi import Depends, Request, HTTPException
from pydantic import BaseModel, Field
from typing import Annotated

from pygments.styles.dracula import yellow

from src.services.auth import AuthService
from src.utils.utils import DbManager
from src.database import AsyncSession


class Pagination(BaseModel):
    limit: int = Field(10, gt=0, lt=20)
    offset: int = Field(0, ge=0)


PaginationDep = Annotated[Pagination, Depends(Pagination)]


def get_token(request: Request) -> str:
    token = request.cookies.get('access_token', None)
    if not token:
        raise HTTPException(status_code=401, detail="Вы не передали токен аутентификации")
    return token

def get_current_user_id(token: str = Depends(get_token)) -> str:
    user_data = AuthService().encode_token(token)
    return user_data['user_id']

AuthUserDep = Annotated[int, Depends(get_current_user_id)]


def get_db_manager():
    return DbManager(session_factory=AsyncSession)

async def get_db():
    async with get_db_manager() as db:
        yield db

DBDep = Annotated[DbManager, Depends(get_db)]