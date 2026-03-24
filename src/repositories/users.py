from src.repositories.base import BaseRepository
from src.repositories.mappers.mappers import UserMapper
from src.models.users import UserOrm
from src.schemas.users import UserHashedPswdSchema
from sqlalchemy import select


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = UserMapper


    async def get_user_with_hashed_pswd(self, username: str):
        query = select(self.model).filter_by(username=username)
        result = await self.session.execute(query)
        result = result.scalars().first()
        return UserHashedPswdSchema.model_validate(result)