from sqlalchemy import select, insert, update, delete
from pydantic import BaseModel


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session


    async def get_objects(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return result.scalars().one_or_none()

    async def add_obj(self, data: BaseModel):
        query = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
                 )

        result = await self.session.execute(query)
        return result.scalar_one()

    async def edit(self, data: BaseModel, id: int):
        exist_one_query = select(self.model).filter_by(id=id)
        res = await self.session.execute(exist_one_query)
        existing_obj = res.scalars().all()
        if not existing_obj:
            raise BaseException(f"Object with id: {id} does not exist in db")

        query = (
            update(self.model)
            .filter_by(id=id)
            .values(**data.model_dump())
            .returning(self.model)
        )

        result = await self.session.execute(query)
        return result.scalar_one()

    async def delete(self, id: int) -> None:
        query = (
            delete(self.model)
            .filter_by(id=id)
        )

        result = await self.session.execute(query)
        return None

    async def edit_bulk(self, data: BaseModel, **filters):
        query = (
            update(self.model)
            .filter_by(**filters)
            .values(**data)
            .returning(self.model)
        )

        result = await self.session.execute(query)
        return result.scalars().all()

    async def delete_bulk(self, **filters):
        query = (
            delete(self.model)
            .filter_by(**filters)
            .returning(self.model)
        )

        result = await self.session.execute(query)
        return result.scalars().all()