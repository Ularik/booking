from src.database import Base
from pydantic import BaseModel
from typing import TypeVar


DbModelType = TypeVar("DbModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseModel)


class DataMapper:
    model: type[DbModelType] = None
    schema: type[SchemaType] = None

    @classmethod
    def map_to_domain_entity(cls, data):
        return cls.schema.model_validate(data)

    @classmethod
    def map_to_persistence_entity(cls, data):
        return cls.model(**data.model_dump())