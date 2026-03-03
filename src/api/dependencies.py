from fastapi import Depends
from pydantic import BaseModel, Field
from typing import Annotated


class Pagination(BaseModel):
    limit: int = Field(10, gt=0, lt=20)
    offset: int = Field(0, ge=0)


PaginationDep = Annotated[Pagination, Depends(Pagination)]